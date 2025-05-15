from flask import Flask
from flask_migrate import Migrate
from app.database import db
from config import Config, TestingConfig
from app.models.token_blacklist import TokenBlacklist

def create_app(testing=False):
    """Create and configure the Flask app."""
    app = Flask(__name__)

    if testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    return app
