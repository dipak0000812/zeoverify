# ai-engine/classifier.py
import pickle
import os
from typing import Tuple

class DocumentClassifier:
    """Document classification using ML models and rule-based detection."""
    
    def __init__(self):
        """Initialize the classifier with ML models if available."""
        self.ml_model = None
        self.vectorizer = None
        self.label_encoder = None
        self.model_loaded = False
        
        # Try to load the trained ML model
        self._load_ml_model()
    
    def _load_ml_model(self):
        """Load the trained ML model if available."""
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'ml_model', 'saved_model')
            
            if os.path.exists(os.path.join(model_path, 'model.safetensors')):
                # Load the trained model
                from transformers import AutoTokenizer, AutoModelForSequenceClassification
                import torch
                
                self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
                
                # Try to load label encoder, but provide fallback if it fails
                try:
                    with open(os.path.join(model_path, 'label_encoder.pkl'), 'rb') as f:
                        self.label_encoder = pickle.load(f)
                except Exception as e:
                    print(f"⚠️ Failed to load label encoder: {e}")
                    print("Using default label mapping")
                    # Create a default label mapping based on model config
                    if hasattr(self.model.config, 'id2label'):
                        self.label_encoder = None
                        self.default_labels = list(self.model.config.id2label.values())
                    else:
                        self.label_encoder = None
                        self.default_labels = ['real_estate', 'fake', 'invalid']
                
                self.model_loaded = True
                print("✅ ML model loaded successfully")
            else:
                print("⚠️ ML model not found, using rule-based classification")
                
        except Exception as e:
            print(f"⚠️ Failed to load ML model: {e}")
            self.model_loaded = False
    
    def is_loaded(self) -> bool:
        """Check if ML model is loaded."""
        return self.model_loaded
    
    def classify_document(self, text: str) -> Tuple[str, float]:
        """
        Classify document type and return confidence score.
        
        Args:
            text: Extracted text from document
            
        Returns:
            Tuple of (document_type, confidence_score)
        """
        if not text.strip():
            return "invalid", 0.0
        
        # Try ML classification first
        if self.model_loaded:
            try:
                return self._ml_classify(text)
            except Exception as e:
                print(f"ML classification failed: {e}")
        
        # Fallback to rule-based classification
        return self._rule_based_classify(text)
    
    def _ml_classify(self, text: str) -> Tuple[str, float]:
        """Classify using trained ML model."""
        import torch
        
        # Tokenize input
        inputs = self.tokenizer(
            text[:512],  # Limit to model's max length
            truncation=True,
            padding=True,
            return_tensors="pt"
        )
        
        # Get prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
        
        # Convert back to original labels
        if self.label_encoder:
            document_type = self.label_encoder.inverse_transform([predicted_class])[0]
        elif hasattr(self, 'default_labels') and predicted_class < len(self.default_labels):
            document_type = self.default_labels[predicted_class]
        else:
            document_type = str(predicted_class)
        
        return document_type, confidence
    
    def _rule_based_classify(self, text: str) -> Tuple[str, float]:
        """Rule-based document classification."""
        text_lower = text.lower()
        
        # Define document type patterns
        patterns = {
            'rera_certificate': [
                'rera', 'real estate regulatory authority', 'certificate', 'registration',
                'maharashtra rera', 'karnataka rera', 'delhi rera'
            ],
            'sale_deed': [
                'sale deed', 'deed of sale', 'conveyance deed', 'property deed',
                'stamp duty', 'sub-registrar', 'plot no', 'survey no'
            ],
            'lease_agreement': [
                'lease agreement', 'rental agreement', 'tenancy agreement',
                'lessor', 'lessee', 'landlord', 'tenant', 'rent'
            ],
            'property_agreement': [
                'property agreement', 'development agreement', 'construction agreement',
                'builder agreement', 'real estate'
            ]
        }
        
        # Calculate scores for each document type
        scores = {}
        for doc_type, keywords in patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[doc_type] = score
        
        # Find the best match
        if scores:
            best_type = max(scores, key=scores.get)
            best_score = scores[best_type]
            
            # Calculate confidence based on score
            total_keywords = len(patterns[best_type])
            confidence = min(1.0, best_score / total_keywords)
            
            if confidence > 0.3:  # Threshold for valid classification
                return best_type, confidence
        
        # Check for invalid/unrelated documents
        invalid_keywords = ['resume', 'cv', 'curriculum vitae', 'job', 'employment', 
                          'tax invoice', 'bill', 'ticket', 'receipt']
        if any(keyword in text_lower for keyword in invalid_keywords):
            return "invalid", 0.8
        
        # Default to unknown
        return "unknown", 0.1

def detect_doc_type(text):
    """Legacy function for backward compatibility."""
    classifier = DocumentClassifier()
    doc_type, confidence = classifier.classify_document(text)
    return doc_type

