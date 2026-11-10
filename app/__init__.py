
import os
from flask import Flask
from app.database import db
from app.routes import main


def create_app():
    app = Flask(__name__)

    # Load secret key from environment variable
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialise database
    db.init_app(app)

    # Register application routes
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
