# ai-engine/ml_model/predict_fixed.py
import joblib
import os
import numpy as np

BASE_DIR = os.path.dirname(__file__)

# Load the existing vectorizer and model
vectorizer = joblib.load(os.path.join(BASE_DIR, 'vectorizer.pkl'))
classifier = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))

DOC_TYPE_MAP = {
    'real_estate': 'real_estate',
    'fake': 'fake',
    'invalid': 'invalid',
}

def predict_doc_type_ml(text: str) -> str:
    """Predict 'real_estate' | 'fake' | 'invalid' using TF-IDF + RandomForest."""
    try:
        # Convert text to TF-IDF features
        features = vectorizer.transform([text])
        
        # Make prediction
        pred = classifier.predict(features)[0]
        return DOC_TYPE_MAP.get(pred, 'invalid')
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return 'invalid'

def predict_doc_type_with_confidence(text: str):
    """Return (label, confidence) where confidence is the max probability (0..1)."""
    try:
        # Convert text to TF-IDF features
        features = vectorizer.transform([text])
        
        # Get prediction probabilities
        probs = classifier.predict_proba(features)[0]
        predicted_class_idx = np.argmax(probs)
        confidence = float(probs[predicted_class_idx])
        
        # Get predicted class
        predicted_class = classifier.classes_[predicted_class_idx]
        readable_label = DOC_TYPE_MAP.get(predicted_class, 'invalid')
        
        return readable_label, confidence
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return 'invalid', 0.0
