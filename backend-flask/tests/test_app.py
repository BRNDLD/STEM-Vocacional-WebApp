"""
Test application factory
"""
import os
import tempfile
from flask import Flask, jsonify
from flask_cors import CORS
from app.models.models import db
from app.routes.usuario_routes import usuario_bp
from app.routes.cognitiva_routes import cognitiva_bp
from app.routes.educativa_familiar_routes import educativa_familiar_bp
from app.routes.socioeconomica_routes import socioeconomica_bp
from app.routes.autoeficacia_routes import autoeficacia_bp
from datetime import datetime

class TestConfig:
    """Test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ENGINE_OPTIONS = {}

def create_test_app(database_uri=None):
    """Create Flask app for testing"""
    app = Flask(__name__)
    
    # Use test configuration
    app.config.from_object(TestConfig)
    
    # Override database URI if provided
    if database_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints (routes)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(cognitiva_bp)
    app.register_blueprint(educativa_familiar_bp)
    app.register_blueprint(socioeconomica_bp)
    app.register_blueprint(autoeficacia_bp)
    
    # Basic routes
    @app.route('/')
    def home():
        return jsonify({'message': 'API STEM Vocacional funcionando con Flask - TEST MODE'})
    
    @app.route('/health')
    def health():
        try:
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'timestamp': datetime.now().isoformat()
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Endpoint no encontrado',
            'error': 'Not Found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor',
            'error': 'Internal Server Error'
        }), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Método no permitido',
            'error': 'Method Not Allowed'
        }), 405
    
    return app