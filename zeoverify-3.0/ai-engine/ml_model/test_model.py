#!/usr/bin/env python3
"""
Test script to verify the trained DistilBERT model works correctly.
"""

import os
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import pickle

# Set the model path
model_path = "saved_model"
BASE_DIR = os.path.dirname(__file__)
full_model_path = os.path.join(BASE_DIR, model_path)

def load_model_and_tokenizer():
    """Load the trained model and tokenizer."""
    print(f"Loading model from: {full_model_path}")
    
    # Check if files exist
    required_files = ['config.json', 'model.safetensors', 'tokenizer.json', 'vocab.txt']
    for file in required_files:
        file_path = os.path.join(full_model_path, file)
        if not os.path.exists(file_path):
            print(f"❌ Missing required file: {file}")
            return None, None
        else:
            print(f"✅ Found: {file}")
    
    try:
        # Load tokenizer and model
        tokenizer = DistilBertTokenizer.from_pretrained(full_model_path)
        model = DistilBertForSequenceClassification.from_pretrained(full_model_path)
        
        # Load label encoder if it exists
        label_encoder_path = os.path.join(full_model_path, 'label_encoder.pkl')
        label_encoder = None
        if os.path.exists(label_encoder_path):
            with open(label_encoder_path, 'rb') as f:
                label_encoder = pickle.load(f)
            print(f"✅ Loaded label encoder: {label_encoder}")
        
        print("✅ Model and tokenizer loaded successfully!")
        return model, tokenizer, label_encoder
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None, None, None

def predict_text(model, tokenizer, text, label_encoder=None):
    """Make prediction on a given text."""
    # Set model to evaluation mode
    model.eval()
    
    # Tokenize input
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    
    # Run prediction
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probs).item()
        confidence = float(probs[0][predicted_class])
    
    # Map prediction to label
    if label_encoder:
        predicted_label = label_encoder.inverse_transform([predicted_class])[0]
    else:
        # Use config labels
        predicted_label = model.config.id2label[predicted_class]
    
    return predicted_label, confidence, probs[0].tolist()

def main():
    """Main test function."""
    print("🧪 Testing DistilBERT Model")
    print("=" * 50)
    
    # Load model
    model, tokenizer, label_encoder = load_model_and_tokenizer()
    if model is None:
        print("❌ Failed to load model. Exiting.")
        return
    
    # Test cases
    test_cases = [
        "This is a real estate document with property details and ownership information.",
        "Fake document with forged signatures and altered dates.",
        "Invalid document that doesn't contain proper information.",
        "Property deed for 123 Main Street, owned by John Doe, dated 2023.",
        "Certificate of authenticity for artwork with gallery stamp."
    ]
    
    print("\n📝 Running Test Predictions:")
    print("-" * 50)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Input: {text[:80]}{'...' if len(text) > 80 else ''}")
        
        try:
            predicted_label, confidence, all_probs = predict_text(model, tokenizer, text, label_encoder)
            print(f"Predicted: {predicted_label}")
            print(f"Confidence: {confidence:.3f}")
            print(f"All probabilities: {[f'{p:.3f}' for p in all_probs]}")
        except Exception as e:
            print(f"❌ Error during prediction: {e}")
    
    print("\n✅ Model test completed!")

if __name__ == "__main__":
    main()
