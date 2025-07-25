# app.py
from flask import Flask, request, jsonify
from ocr_engine import extract_text_from_image
from fraud_detector import detect_fraud

app = Flask(__name__)

@app.route('/verify-document', methods=['POST'])
def verify_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    image_bytes = file.read()

    print("[INFO] Extracting text from image...")
    text = extract_text_from_image(image_bytes)
    print(f"[INFO] Extracted Text:\n{text}")

    print("[INFO] Running fraud detection...")
    is_fraud = detect_fraud(text)

    return jsonify({
        'extracted_text': text,
        'fraud_detected': is_fraud
    })

if __name__ == '__main__':
    app.run(debug=True)
