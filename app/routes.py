# app/routes.py
from flask import Blueprint,send_from_directory
from .database import db
from .models import User
from marshmallow import Schema, fields, validate, ValidationError
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
#test
import base64
import json
from PIL import Image
from scipy.io.wavfile import write
import numpy as np
import wave

import io

bp = Blueprint('user', __name__)
user_api_URL_prefix='/api/v1'

class SignUpUserSchema(Schema):
    user_email = fields.Email(required=True)
    user_password = fields.Str(required=True, validate=validate.Length(min=6))

sign_up_user_schema = SignUpUserSchema()
@bp.route('/user/add_user', methods=['POST'])
def add_user():
    data = request.json
    try:
        # Validate and deserialize input
        hashed_password = generate_password_hash(data['user_password'])
        new_user = User(
             user_email=data['user_email'],
             user_password=hashed_password  # Store the hashed password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'}), 201
    except ValidationError as ve:
        return jsonify({'error': str(ve.messages)}), 400
    except IntegrityError as ie:
        db.session.rollback()
        return jsonify({'error': 'This email is already in use.'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/user/get_user_info', methods=['GET'])
def get_user_info():
    user_id = request.args.get('user_id', type=int)
    if user_id:
        # Fetch specific user data
        user = User.query.get(user_id)
        if user:
            user_info = {
                "user_id": user.user_id,
                "user_first_name": user.user_first_name,
                "user_last_name": user.user_last_name,
                "user_email": user.user_email,
                "user_phone": user.user_phone,
                "user_address": user.user_address,
                "user_enable_status": user.user_enable_status,
                "user_signup_at": user.user_signup_at.isoformat() if user.user_signup_at else None,
                "user_last_change_code_time": user.user_last_change_code_time.isoformat() if user.user_last_change_code_time else None,
                "user_mobile_bar_code": user.user_mobile_bar_code
            }
            return jsonify(user_info), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        # Fetch all users data
        users = User.query.all()
        users_info = [{
            "user_id": user.user_id,
            "user_first_name": user.user_first_name,
            "user_last_name": user.user_last_name,
            "user_email": user.user_email,
            "user_phone": user.user_phone,
            "user_address": user.user_address,
            "user_enable_status": user.user_enable_status,
            "user_signup_at": user.user_signup_at.isoformat() if user.user_signup_at else None,
            "user_last_change_code_time": user.user_last_change_code_time.isoformat() if user.user_last_change_code_time else None,
            "user_mobile_bar_code": user.user_mobile_bar_code
        } for user in users]
        return jsonify(users_info), 200


@bp.route('/image/process_and_generate_sound', methods=['POST'])
def process_image_and_generate_sound():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    try:
        # Read the image from the file storage and decode it
        image_bytes = file.read()
        encoded_string = base64.b64encode(image_bytes).decode('utf-8')
        
        # Decode the image for processing
        image_data = base64.b64decode(encoded_string)
        image = Image.open(io.BytesIO(image_data))
        image_array = np.array(image)

        # Calculate the average color and use it to define a frequency
        average_color = np.mean(image_array, axis=(0, 1))
        frequency = np.mean(average_color)  # Convert average color to a frequency

        # Generate a sine wave based on the frequency
        samplerate = 44100  # Audio sample rate
        duration = 5  # Duration in seconds
        t = np.linspace(0, duration, int(samplerate * duration))
        audio = 0.5 * np.sin(2 * np.pi * frequency * t)

        # Write the audio data to a WAV file (not MP3 directly)
        output_filename = 'output.wav'
        write(output_filename, samplerate, audio.astype(np.float32))

        # Return success response
        audio_list = audio.astype(np.float32).tolist()  # Convert NumPy array to list
        return jsonify({
    'message': 'Audio generated successfully',
    'audio_file': output_filename,
    'sample_rate': samplerate,
    'audio_data': audio_list
    }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@bp.route('/audio/audio_to_image', methods=['POST'])
def audio_to_image():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio provided.'}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    try:
        # Read and process the audio file
        with wave.open(file, 'rb') as wav_file:  # Use 'rb' mode for reading binary
            frames = wav_file.readframes(wav_file.getnframes())
            audio_array = np.frombuffer(frames, dtype=np.int16)
        
        # Normalize and reshape the audio data to create an image
        max_val = np.iinfo(np.int16).max
        audio_normalized = 255 * ((audio_array + abs(audio_array.min())) / (2 * max_val))
        desired_length = 512 * 512  # Image size is 512x512
        if len(audio_normalized) < desired_length:
            audio_normalized = np.pad(audio_normalized, (0, desired_length - len(audio_normalized)), 'constant')
        audio_normalized = audio_normalized[:desired_length]  # Ensure the array fits the image size exactly
        image_data = audio_normalized.reshape((512, 512))

        # Create an image from the array
        image = Image.fromarray(np.uint8(image_data))
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)  # Reset buffer position to the beginning

        # Encode image to base64 string
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        # Return JSON response
        return jsonify({'image_base64': img_base64}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        

@bp.routeroute('/', methods=['GET'])
def helloworld():
    return "Hello World!"
