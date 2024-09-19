from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    Bootstrap(app)

    # Import blueprints (controllers)
    from .controllers import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Create the database
    with app.app_context():
        db.create_all()

    return app
