"""
ZeoVerify 3.0 AI Engine API
Modular Flask application for document verification with AI and blockchain integration.
"""

from flask import Flask
from flask_cors import CORS
import logging

def create_app():
    """Application factory pattern for Flask app."""
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Enable CORS
    CORS(app)
    
    # Import and register routes
    from .routes import api_bp
    app.register_blueprint(api_bp)
    
    return app
