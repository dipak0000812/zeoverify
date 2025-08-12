#!/usr/bin/env python3
"""
Main Flask API for ZeoVerify 3.0
Handles document verification, OCR, AI classification, and blockchain integration.
"""

import os
import sys
import logging
from flask import Flask
from flask_cors import CORS

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Import and register the API blueprint
    try:
        from routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        logger.info("✅ API blueprint registered successfully")
    except Exception as e:
        logger.error(f"❌ Failed to register API blueprint: {e}")
        raise
    
    # Add a root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return {
            "message": "ZeoVerify 3.0 API",
            "version": "3.0.0",
            "status": "running",
            "endpoints": {
                "health": "/api/health",
                "verify": "/api/verify",
                "verify_text": "/api/verify-text",
                "blockchain_status": "/api/blockchain/status",
                "verification_history": "/api/verify/history"
            }
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Endpoint not found"}, 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return {"error": "Method not allowed"}, 405

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500
    
    return app

def initialize_app():
    """Initialize the application and its components."""
    try:
        app = create_app()
        logger.info("✅ Flask application created successfully")
        return app
    except Exception as e:
        logger.error(f"❌ Failed to create Flask application: {e}")
        raise

if __name__ == "__main__":
    try:
        # Create the application
        app = initialize_app()
        
        # Get port from environment
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_ENV') == 'development'
        
        logger.info(f"🚀 Starting ZeoVerify 3.0 API on port {port}")
        logger.info(f"📋 Available endpoints:")
        logger.info(f"   GET  http://localhost:{port}/")
        logger.info(f"   GET  http://localhost:{port}/api/health")
        logger.info(f"   POST http://localhost:{port}/api/verify")
        logger.info(f"   POST http://localhost:{port}/api/verify-text")
        logger.info(f"   GET  http://localhost:{port}/api/blockchain/status")
        logger.info(f"   GET  http://localhost:{port}/api/verify/history")
        
        # Start the server
        app.run(host='0.0.0.0', port=port, debug=debug)
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Error starting server: {e}")
        sys.exit(1)
