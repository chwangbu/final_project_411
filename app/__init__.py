from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import session
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback-secret-key")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.permanent_session_lifetime = timedelta(minutes=15) #15 min session timeout

    db.init_app(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app