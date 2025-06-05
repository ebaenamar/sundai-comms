from flask import Flask, request, jsonify, make_response, current_app, redirect
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuración básica de CORS
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Cache-Control", "Pragma", "Expires", "X-Forwarded-Proto", "X-Request-ID"],
            "expose_headers": ["Content-Type", "Content-Length", "Authorization", "X-Requested-With", "X-Request-ID"],
            "supports_credentials": False,
            "max_age": 86400
        }
    })
    
    # Forzar HTTPS en producción
    @app.before_request
    def force_https():
        # No redirigir si ya es HTTPS o si es una solicitud OPTIONS
        if request.url.startswith('http://') and request.method != 'OPTIONS':
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)
            
        # Para solicitudes OPTIONS, devolver una respuesta vacía con las cabeceras CORS
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Cache-Control, Pragma, Expires, X-Forwarded-Proto, X-Request-ID')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Max-Age', '86400')
            response.headers.add('Vary', 'Origin, Access-Control-Request-Method, Access-Control-Request-Headers')
            return response, 200
    
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
