from flask import Flask, redirect, url_for
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
    # from .controllers import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    # Import the controllers
    from .controllers.home_controller import home
    from .controllers.asset_controller import asset
    from .controllers.issuance_controller import issuance
    from .controllers.user_controller import user
    from .controllers.dashboard_controller import dashboard

    # Register Blueprints
    app.register_blueprint(home, url_prefix='/home')
    app.register_blueprint(asset, url_prefix='/assets')
    app.register_blueprint(issuance, url_prefix='/issuances')
    app.register_blueprint(user, url_prefix='/users')
    app.register_blueprint(dashboard, url_prefix='/dashboard')

    # This will redirect localhost:5000/ to localhost:5000/home
    @app.route('/')
    def index():
        return redirect(url_for('home.home_page'))

    # Create the database
    with app.app_context():
        db.create_all()

    return app
