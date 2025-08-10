#!/usr/bin/env python3
"""
Flask API for certificate verification using trained transformer model.
"""

import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class CertificateVerifier:
    """Certificate verification model wrapper."""
    
    def __init__(self, model_path):
        """Initialize the model and tokenizer."""
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.label_mapping = {
            'LABEL_0': 'real_estate',
            'LABEL_1': 'fake',
            'LABEL_2': 'invalid'
        }
        self.load_model()
    
    def load_model(self):
        """Load the trained model and tokenizer."""
        try:
            logger.info(f"Loading model from: {self.model_path}")
            
            # Check if model files exist
            required_files = ['config.json', 'model.safetensors', 'tokenizer.json', 'vocab.txt']
            for file in required_files:
                file_path = os.path.join(self.model_path, file)
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Missing required file: {file}")
            
            # Load tokenizer and model
            self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_path)
            self.model = DistilBertForSequenceClassification.from_pretrained(self.model_path)
            
            # Set model to evaluation mode
            self.model.eval()
            
            logger.info("✅ Model loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            raise
    
    def predict(self, text):
        """Make prediction on certificate text."""
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512, 
                padding=True
            )
            
            # Run prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
                predicted_class = torch.argmax(probs).item()
                confidence = float(probs[0][predicted_class])
            
            # Map prediction to readable label
            predicted_label = self.model.config.id2label[predicted_class]
            readable_label = self.label_mapping.get(predicted_label, predicted_label)
            
            return {
                'status': readable_label,
                'confidence': confidence,
                'probabilities': probs[0].tolist()
            }
            
        except Exception as e:
            logger.error(f"❌ Error during prediction: {e}")
            raise

# Initialize the verifier
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_model', 'saved_model')
verifier = None

def initialize_verifier():
    """Initialize the certificate verifier."""
    global verifier
    try:
        verifier = CertificateVerifier(MODEL_PATH)
        return True
    except Exception as e:
        logger.error(f"Failed to initialize verifier: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "running",
        "model_loaded": verifier is not None
    })

@app.route('/verify', methods=['POST'])
def verify_certificate():
    """Verify certificate endpoint."""
    try:
        # Check if model is loaded
        if verifier is None:
            return jsonify({
                "error": "Model not loaded. Please check server logs."
            }), 500
        
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400
        
        # Extract certificate text
        certificate_text = data.get('certificate_text', '').strip()
        if not certificate_text:
            return jsonify({
                "error": "certificate_text field is required and cannot be empty"
            }), 400
        
        # Make prediction
        result = verifier.predict(certificate_text)
        
        # Return result
        return jsonify({
            "status": result['status'],
            "confidence": result['confidence'],
            "message": f"Certificate classified as {result['status']} with {result['confidence']:.2%} confidence"
        })
        
    except Exception as e:
        logger.error(f"Error in verify endpoint: {e}")
        return jsonify({
            "error": "Internal server error during verification"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        "error": "Method not allowed"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "error": "Internal server error"
    }), 500

if __name__ == "__main__":
    # Initialize the verifier
    if not initialize_verifier():
        logger.error("Failed to initialize verifier. Exiting.")
        sys.exit(1)
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
