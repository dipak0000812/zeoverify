#!/usr/bin/env python3
"""
Simple Flask API for certificate verification using existing predict.py module.
This version only uses the new AI model (TF-IDF + RandomForest) to avoid dependency conflicts.
"""

import os
import sys
import logging
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Request logging middleware
@app.before_request
def log_request_info():
    """Log all incoming requests for debugging."""
    logger.info(f"Request: {request.method} {request.path} - IP: {request.remote_addr}")

@app.after_request
def log_response_info(response):
    """Log all outgoing responses for debugging."""
    logger.info(f"Response: {response.status_code} for {request.method} {request.path}")
    return response

# Import the fixed prediction functions
try:
    from ml_model.predict_fixed import predict_doc_type_ml, predict_doc_type_with_confidence
    model_loaded = True
    logger.info("✅ Successfully imported prediction functions")
except Exception as e:
    logger.error(f"❌ Error importing prediction functions: {e}")
    model_loaded = False

# Create upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage for verification history (in production, use a database)
verification_history = []

def extract_text_from_file(filepath, filename):
    """Extract text from uploaded file (PDF or image)."""
    try:
        file_extension = filename.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            # Extract text from PDF
            try:
                import PyPDF2
                with open(filepath, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    return text.strip() if text.strip() else "No text extracted from PDF"
            except ImportError:
                logger.warning("PyPDF2 not available, using fallback text extraction")
                return f"PDF document: {filename} (text extraction not available)"
            except Exception as e:
                logger.error(f"PDF text extraction error: {e}")
                return f"PDF document: {filename} (extraction failed)"
        
        elif file_extension in ['jpg', 'jpeg', 'png']:
            # Extract text from images using OCR
            try:
                import pytesseract
                from PIL import Image
                import cv2
                import numpy as np
                
                # Read image using OpenCV
                image = cv2.imread(filepath)
                if image is None:
                    return f"Image document: {filename} (failed to read image)"
                
                # Convert to grayscale for better OCR
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                # Apply preprocessing to improve OCR accuracy
                # Remove noise
                denoised = cv2.medianBlur(gray, 3)
                
                # Apply thresholding to get better contrast
                _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                # Try OCR with different preprocessing methods
                ocr_text = ""
                
                # Method 1: Direct OCR on grayscale
                try:
                    ocr_text = pytesseract.image_to_string(gray, lang='eng')
                except:
                    pass
                
                # Method 2: OCR on thresholded image if first method fails
                if not ocr_text.strip():
                    try:
                        ocr_text = pytesseract.image_to_string(thresh, lang='eng')
                    except:
                        pass
                
                # Method 3: OCR on denoised image if previous methods fail
                if not ocr_text.strip():
                    try:
                        ocr_text = pytesseract.image_to_string(denoised, lang='eng')
                    except:
                        pass
                
                # Clean up the extracted text
                if ocr_text.strip():
                    # Remove extra whitespace and normalize
                    cleaned_text = ' '.join(ocr_text.split())
                    logger.info(f"Successfully extracted text from {filename} using OCR")
                    return cleaned_text
                else:
                    # If no text found, return image info
                    with Image.open(filepath) as img:
                        width, height = img.size
                        mode = img.mode
                    return f"Image document: {filename} ({width}x{height}, {mode}) - No text detected via OCR"
                    
            except ImportError as e:
                logger.warning(f"OCR dependencies not available: {e}")
                return f"Image document: {filename} (OCR not available - install pytesseract, opencv-python, and Pillow)"
            except Exception as e:
                logger.error(f"OCR processing error: {e}")
                return f"Image document: {filename} (OCR processing failed: {str(e)})"
        
        else:
            return f"Unsupported file type: {file_extension}"
            
    except Exception as e:
        logger.error(f"Text extraction error: {e}")
        return f"Document: {filename} (extraction failed: {str(e)})"

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "running",
        "model_loaded": model_loaded
    })

@app.route('/verify', methods=['POST'])
def verify_certificate():
    """Verify certificate endpoint - accepts JSON with certificate_text."""
    try:
        # Check if model is loaded
        if not model_loaded:
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
        
        # Make prediction using existing functions
        try:
            status, confidence = predict_doc_type_with_confidence(certificate_text)
            
            # Return result
            return jsonify({
                "status": status,
                "confidence": confidence,
                "message": f"Certificate classified as {status} with {confidence:.2%} confidence"
            })
            
        except Exception as pred_error:
            logger.error(f"Prediction error: {pred_error}")
            return jsonify({
                "error": "Error during prediction"
            }), 500
        
    except Exception as e:
        logger.error(f"Error in verify endpoint: {e}")
        return jsonify({
            "error": "Internal server error during verification"
        }), 500

@app.route('/api/verify', methods=['POST'])
def verify_document():
    """Verify document endpoint - accepts file upload (compatible with frontend)."""
    try:
        # Check if model is loaded
        if not model_loaded:
            return jsonify({
                "error": "Model not loaded. Please check server logs."
            }), 500
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                "error": "No file uploaded"
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                "error": "No file selected"
            }), 400
        
        # Validate file type
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
        file_extension = file.filename.lower().split('.')[-1]
        if file_extension not in allowed_extensions:
            return jsonify({
                "error": f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            }), 400
        
        # Validate file size (5MB limit)
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > 5 * 1024 * 1024:  # 5MB
            return jsonify({
                "error": "File size must be less than 5MB"
            }), 400
        
        # Save file temporarily
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        try:
            # Extract actual text from the uploaded file
            extracted_text = extract_text_from_file(filepath, file.filename)
            
            # Make ML prediction using the new AI model
            doc_type_ml, doc_conf = predict_doc_type_with_confidence(extracted_text)
            
            # Determine fraud risk based on confidence
            if doc_conf >= 0.8:
                fraud_risk = "Low"
                fraud_risk_percent = 15.0
            elif doc_conf >= 0.6:
                fraud_risk = "Medium"
                fraud_risk_percent = 45.0
            else:
                fraud_risk = "High"
                fraud_risk_percent = 85.0
            
            # Generate fraud issues based on confidence
            fraud_issues = []
            if doc_conf < 0.7:
                fraud_issues.append("Low confidence in document classification")
            if doc_conf < 0.5:
                fraud_issues.append("Document may be fraudulent or corrupted")
            
            # Generate file hash
            with open(filepath, "rb") as f:
                file_hash = "0x" + hashlib.sha256(f.read()).hexdigest()
            
            # Store verification result in history
            verification_record = {
                "id": len(verification_history) + 1,
                "filename": file.filename,
                "verifiedAt": datetime.now().isoformat(),
                "fraudRisk": fraud_risk_percent,
                "result": "Genuine" if fraud_risk == "Low" else "Invalid",
                "documentType": doc_type_ml,
                "extractedText": extracted_text,
                "fraudIssues": fraud_issues,
                "fileHash": file_hash,
                "doc_confidence": round(doc_conf * 100, 2)
            }
            
            verification_history.append(verification_record)
            
            # Clean up temporary file
            try:
                os.remove(filepath)
            except:
                pass
            
            # Return response in the format expected by frontend
            return jsonify({
                "filename": file.filename,
                "doc_type_ml": doc_type_ml,
                "doc_type_rule": "ml_model_only",
                "fraud_risk": fraud_risk,
                "doc_confidence": round(doc_conf * 100, 2),
                "fraud_risk_percent": fraud_risk_percent,
                "fraud_issues": fraud_issues,
                "extracted_text": extracted_text,
                "file_hash": file_hash,
                "verification_id": verification_record["id"]
            })
            
        except Exception as processing_error:
            logger.error(f"Error processing file: {processing_error}")
            # Clean up temporary file
            try:
                os.remove(filepath)
            except:
                pass
            return jsonify({
                "error": "Error processing document"
            }), 500
        
    except Exception as e:
        logger.error(f"Error in verify document endpoint: {e}")
        return jsonify({
            "error": "Internal server error during verification"
        }), 500

@app.route('/verify-simple', methods=['POST'])
def verify_certificate_simple():
    """Simple verification endpoint without confidence."""
    try:
        # Check if model is loaded
        if not model_loaded:
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
        
        # Make simple prediction
        try:
            status = predict_doc_type_ml(certificate_text)
            
            # Return result
            return jsonify({
                "status": status,
                "message": f"Certificate classified as {status}"
            })
            
        except Exception as pred_error:
            logger.error(f"Prediction error: {pred_error}")
            return jsonify({
                "error": "Error during prediction"
            }), 500
        
    except Exception as e:
        logger.error(f"Error in verify endpoint: {e}")
        return jsonify({
            "error": "Internal server error during verification"
        }), 500

@app.route('/api/verify/history', methods=['GET'])
def get_verification_history():
    """Get verification history endpoint."""
    try:
        return jsonify({
            "success": True,
            "data": verification_history,
            "total": len(verification_history)
        })
    except Exception as e:
        logger.error(f"Error fetching verification history: {e}")
        return jsonify({
            "error": "Failed to fetch verification history"
        }), 500

@app.route('/api/verify/history/<int:verification_id>', methods=['GET'])
def get_verification_by_id(verification_id):
    """Get specific verification by ID."""
    try:
        verification = next((v for v in verification_history if v["id"] == verification_id), None)
        if not verification:
            return jsonify({
                "error": "Verification not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": verification
        })
    except Exception as e:
        logger.error(f"Error fetching verification: {e}")
        return jsonify({
            "error": "Failed to fetch verification"
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
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask API on port {port}")
    logger.info(f"Model loaded: {model_loaded}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
