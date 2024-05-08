import unittest
from flask import json
from app.main import app  # Adjust this import based on where your Flask app is initialized
from app.models import db, User

class APITestCase(unittest.TestCase):
    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for tests
        self.app = app.test_client()

        # Set up the database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_user(self):
        # Sample data to send as POST request
        user_data = {
            'user_id': 'testuser123',
            'user_first_name': 'John',
            'user_last_name': 'Doe',
            'user_email': 'johndoe@example.com',
            'user_phone': '1234567890',
            'user_address': '1234 Test St',
            'user_enable_status': True,
            'user_sign_up_at': '2023-01-01',
            'user_last_change_code_time': '2023-01-02',
            'user_mobile_bar_code': 'barcode123',
            'user_password': 'securepassword'
        }

        # Send POST request and capture the response
        response = self.app.post('/add_user', data=json.dumps(user_data), content_type='application/json')

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Check if the message returned is correct
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'User added successfully')

        # Further check: Ensure user is actually added to the database
        with app.app_context():
            user = User.query.filter_by(user_id='testuser123').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.user_email, 'johndoe@example.com')

if __name__ == '__main__':
    unittest.main()
