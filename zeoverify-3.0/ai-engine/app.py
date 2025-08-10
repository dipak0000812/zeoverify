from flask import Flask, request, jsonify
from ocr import extract_text
from fraud_checker import check_fraud
from ml_model.predict import predict_doc_type_ml
import hashlib
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/verify-document', methods=['POST'])
def verify_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # OCR
    text = extract_text(filepath)

    # ML
    doc_type_ml = predict_doc_type_ml(text)

    # Fraud check
    fraud_risk, fraud_issues = check_fraud(text)

    # Blockchain proof (simulate: hash)
    with open(filepath, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    return jsonify({
        "document_type_ml": doc_type_ml,
        "fraud_risk": fraud_risk,
        "fraud_issues": fraud_issues,
        "extracted_text": text,
        "file_hash": file_hash
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
