from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        MONGO_URI=os.environ.get('MONGO_URI', 'mongodb://localhost:27017/tally_subscribers'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    from app.routes import webhook_bp, subscribers_bp, newsletter_bp
    app.register_blueprint(webhook_bp)
    app.register_blueprint(subscribers_bp)
    app.register_blueprint(newsletter_bp)

    return app
