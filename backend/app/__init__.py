from flask import Flask, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuración de CORS para permitir todas las conexiones
    CORS(app, resources={
        r"/*": {
            "origins": "*",  # Permitir todos los orígenes
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["*"],  # Permitir todas las cabeceras
            "expose_headers": ["*"],  # Exponer todas las cabeceras
            "supports_credentials": False,
            "max_age": 86400,  # 24 horas
            "automatic_options": True
        }
    })
    
    # Forzar HTTPS en producción
    @app.before_request
    def force_https():
        # Solo en producción
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)
    
    # Manejar manualmente las solicitudes OPTIONS para evitar redirecciones
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            headers = {}
            headers['Access-Control-Allow-Origin'] = '*'
            headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
            headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Cache-Control, Pragma, Expires, X-Forwarded-Proto, X-Request-ID'
            headers['Access-Control-Expose-Headers'] = 'Content-Type, Content-Length, Authorization, X-Requested-With, X-Request-ID'
            headers['Access-Control-Max-Age'] = '86400'
            headers['Vary'] = 'Origin, Access-Control-Request-Method, Access-Control-Request-Headers'
            headers['X-Forwarded-Proto'] = 'https'
            headers['X-Forwarded-Ssl'] = 'on'
            return response, 200, headers
    
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
