from flask import Flask
from flask_cors import CORS
from .config import Config
from .database import db
from .routes import bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*","https://help-transfer-cryptos-front-page.pages.dev/":"*"}})
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(bp, url_prefix='/api/v1')

    return app