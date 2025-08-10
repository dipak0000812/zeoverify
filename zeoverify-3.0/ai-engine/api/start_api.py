#!/usr/bin/env python3
"""
Startup script for the Certificate Verification API.
Handles environment setup and starts the Flask server.
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_model_files():
    """Check if required model files exist."""
    model_path = os.path.join(os.path.dirname(__file__), '..', 'ml_model', 'saved_model')
    required_files = ['config.json', 'model.safetensors', 'tokenizer.json', 'vocab.txt']
    
    print(f"🔍 Checking model files in: {model_path}")
    
    for file in required_files:
        file_path = os.path.join(model_path, file)
        if os.path.exists(file_path):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
            return False
    
    return True

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import flask
        import torch
        import transformers
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        return False

def setup_environment():
    """Setup environment variables."""
    # Set default port if not already set
    if 'PORT' not in os.environ:
        os.environ['PORT'] = '5000'
    
    # Set Flask environment
    if 'FLASK_ENV' not in os.environ:
        os.environ['FLASK_ENV'] = 'development'
    
    print(f"🌍 Environment: PORT={os.environ['PORT']}, FLASK_ENV={os.environ['FLASK_ENV']}")

def start_server():
    """Start the Flask server."""
    print("\n🚀 Starting Certificate Verification API...")
    print("=" * 50)
    
    try:
        # Import and run the app
        from app import app, initialize_verifier
        
        # Initialize the verifier
        if not initialize_verifier():
            print("❌ Failed to initialize certificate verifier")
            return False
        
        # Get port from environment
        port = int(os.environ.get('PORT', 5000))
        
        print(f"✅ API starting on http://localhost:{port}")
        print("📋 Available endpoints:")
        print(f"   GET  http://localhost:{port}/health")
        print(f"   POST http://localhost:{port}/verify")
        print("\n🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start the server
        app.run(host='0.0.0.0', port=port, debug=True)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main startup function."""
    print("🔧 Certificate Verification API Startup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_model_files():
        print("\n❌ Model files are missing. Please ensure the model is trained and saved.")
        sys.exit(1)
    
    if not check_dependencies():
        print("\n❌ Dependencies are missing. Please install them first.")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Start server
    if not start_server():
        sys.exit(1)

if __name__ == "__main__":
    main()
