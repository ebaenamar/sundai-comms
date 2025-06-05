from flask import Flask, request, jsonify, make_response, current_app, redirect
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuración mínima de CORS - El manejo detallado se hará manualmente
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    @app.before_request
    def handle_cors():
        # Si es una solicitud OPTIONS, responder inmediatamente con las cabeceras CORS
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Cache-Control, Pragma, Expires, X-Forwarded-Proto, X-Request-ID')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Max-Age', '86400')
            response.headers.add('Vary', 'Origin, Access-Control-Request-Method, Access-Control-Request-Headers')
            return response, 200
            
        # Añadir cabeceras CORS a todas las respuestas
        @app.after_request
        def add_cors_headers(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Cache-Control, Pragma, Expires, X-Forwarded-Proto, X-Request-ID')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Max-Age', '86400')
            response.headers.add('Vary', 'Origin, Access-Control-Request-Method, Access-Control-Request-Headers')
            return response
    
    # El manejo de OPTIONS ahora se hace en force_https
    
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
