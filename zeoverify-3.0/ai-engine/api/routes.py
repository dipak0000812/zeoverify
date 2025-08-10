"""
API routes for ZeoVerify 3.0 AI Engine
Handles document verification, OCR, AI classification, and blockchain integration.
"""

import os
import hashlib
import logging
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import tempfile

# Import our modular components
from ..ocr import extract_text_from_file
from ..classifier import DocumentClassifier
from ..fraud_checker import FraudDetector
from ..blockchain_utils import BlockchainManager

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__)

# Initialize components
classifier = DocumentClassifier()
fraud_detector = FraudDetector()
blockchain_manager = BlockchainManager()

# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        return jsonify({
            "status": "running",
            "model_loaded": classifier.is_loaded(),
            "blockchain_connected": blockchain_manager.is_connected()
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/verify', methods=['POST'])
def verify_document():
    """
    Main document verification endpoint.
    Accepts file upload, processes with OCR, AI classification, and fraud detection.
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed"}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_filepath)
        
        try:
            # Step 1: Extract text using OCR
            logger.info(f"Processing file: {filename}")
            extracted_text = extract_text_from_file(temp_filepath)
            
            if not extracted_text.strip():
                return jsonify({"error": "Could not extract text from document"}), 400
            
            # Step 2: AI Document Classification
            ml_document_type, ml_confidence = classifier.classify_document(extracted_text)
            
            # Step 3: Fraud Detection
            fraud_risk, issues = fraud_detector.analyze_document(extracted_text)
            
            # Step 4: Generate document hash
            with open(temp_filepath, "rb") as f:
                document_hash = "0x" + hashlib.sha256(f.read()).hexdigest()
            
            # Step 5: Store hash on blockchain (if connected)
            blockchain_tx_hash = None
            if blockchain_manager.is_connected():
                try:
                    blockchain_tx_hash = blockchain_manager.store_verification_result(
                        document_hash=document_hash,
                        document_type=ml_document_type,
                        fraud_risk=fraud_risk,
                        confidence=ml_confidence
                    )
                except Exception as e:
                    logger.warning(f"Blockchain storage failed: {e}")
            
            # Clean up temporary file
            try:
                os.remove(temp_filepath)
            except Exception as e:
                logger.warning(f"Failed to clean up temp file: {e}")
            
            # Return comprehensive response
            response = {
                "extracted_text": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
                "ml_document_type": ml_document_type,
                "ml_confidence": round(ml_confidence * 100, 2),
                "fraud_risk": fraud_risk,
                "issues": issues,
                "document_hash": document_hash,
                "blockchain_tx_hash": blockchain_tx_hash,
                "filename": filename
            }
            
            logger.info(f"Document verification completed: {ml_document_type} ({ml_confidence:.2%} confidence)")
            return jsonify(response)
            
        except Exception as processing_error:
            logger.error(f"Error processing document: {processing_error}")
            # Clean up temporary file
            try:
                os.remove(temp_filepath)
            except:
                pass
            return jsonify({"error": "Error processing document"}), 500
        
    except Exception as e:
        logger.error(f"Error in verify endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@api_bp.route('/verify-text', methods=['POST'])
def verify_text():
    """Verify document from text input (no file upload)."""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Text input required"}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400
        
        # Process text directly
        ml_document_type, ml_confidence = classifier.classify_document(text)
        fraud_risk, issues = fraud_detector.analyze_document(text)
        
        # Generate hash from text
        document_hash = "0x" + hashlib.sha256(text.encode()).hexdigest()
        
        response = {
            "extracted_text": text,
            "ml_document_type": ml_document_type,
            "ml_confidence": round(ml_confidence * 100, 2),
            "fraud_risk": fraud_risk,
            "issues": issues,
            "document_hash": document_hash
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in text verification: {e}")
        return jsonify({"error": "Internal server error"}), 500

@api_bp.route('/blockchain/status', methods=['GET'])
def blockchain_status():
    """Check blockchain connection status."""
    try:
        return jsonify({
            "connected": blockchain_manager.is_connected(),
            "network": blockchain_manager.get_network_info()
        })
    except Exception as e:
        logger.error(f"Blockchain status error: {e}")
        return jsonify({"error": str(e)}), 500

@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404

@api_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({"error": "Method not allowed"}), 405

@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500
