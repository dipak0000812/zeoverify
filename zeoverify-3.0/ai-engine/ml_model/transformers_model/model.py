"""
Transformer-based model for Zeoverify Document Verification
Handles model architecture, loading, and inference
"""

import torch
import torch.nn as nn
from transformers import (
    AutoModel, 
    AutoTokenizer, 
    AutoConfig,
    AutoModelForSequenceClassification
)
from typing import Dict, Any, Optional, Tuple, List
import numpy as np
from pathlib import Path
import json
import pickle

from ..config import MODEL_CONFIG, SAVED_MODEL_DIR, SAVED_TOKENIZER_PATH
from ..preprocessing import TextPreprocessor

class DocumentVerificationModel(nn.Module):
    """Transformer-based model for document verification"""
    
    def __init__(self, model_name: str = None, num_labels: int = 2, dropout: float = 0.1):
        super(DocumentVerificationModel, self).__init__()
        
        self.model_name = model_name or MODEL_CONFIG["model_name"]
        self.num_labels = num_labels
        self.dropout = dropout
        
        # Load pre-trained transformer
        self.transformer = AutoModel.from_pretrained(self.model_name)
        
        # Classification head
        hidden_size = self.transformer.config.hidden_size
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, num_labels)
        )
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize classifier weights"""
        for module in self.classifier.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
    
    def forward(self, input_ids, attention_mask=None, token_type_ids=None, labels=None):
        """Forward pass"""
        # Get transformer outputs
        outputs = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids
        )
        
        # Use [CLS] token representation
        pooled_output = outputs.pooler_output
        
        # Classification
        logits = self.classifier(pooled_output)
        
        outputs = (logits,)
        
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
            outputs = (loss,) + outputs
        
        return outputs

class ModelManager:
    """Manages model loading, saving, and inference"""
    
    def __init__(self, model_dir: Path = None):
        self.model_dir = model_dir or SAVED_MODEL_DIR
        self.model = None
        self.tokenizer = None
        self.config = None
        self.label_encoder = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def load_model(self, model_path: str = None) -> bool:
        """Load the trained model"""
        try:
            if model_path is None:
                model_path = self.model_dir / "model.safetensors"
            
            if not Path(model_path).exists():
                print(f"❌ Model not found at {model_path}")
                return False
            
            # Load model configuration
            config_path = self.model_dir / "config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
            
            # Load tokenizer
            tokenizer_path = self.model_dir / "tokenizer.json"
            if tokenizer_path.exists():
                self.tokenizer = AutoTokenizer.from_pretrained(str(self.model_dir))
            else:
                # Fall back to default tokenizer
                model_name = self.config.get("model_name", MODEL_CONFIG["model_name"]) if self.config else MODEL_CONFIG["model_name"]
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Load model
            self.model = DocumentVerificationModel(
                model_name=self.config.get("model_name", MODEL_CONFIG["model_name"]) if self.config else MODEL_CONFIG["model_name"],
                num_labels=self.config.get("num_labels", 2) if self.config else 2
            )
            
            # Load weights
            if str(model_path).endswith('.safetensors'):
                from safetensors.torch import load_file
                state_dict = load_file(model_path)
            else:
                state_dict = torch.load(model_path, map_location=self.device)
            
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            
            # Load label encoder
            encoder_path = self.model_dir / "label_encoder.pkl"
            if encoder_path.exists():
                with open(encoder_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
            
            print(f"✅ Model loaded successfully from {model_path}")
            print(f"🖥️  Using device: {self.device}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def predict(self, text: str, return_probs: bool = False) -> Dict[str, Any]:
        """Predict document authenticity"""
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        try:
            # Preprocess text
            preprocessor = TextPreprocessor()
            tokenized = preprocessor.tokenize_text(text)
            
            # Move to device
            input_ids = tokenized["input_ids"].to(self.device)
            attention_mask = tokenized["attention_mask"].to(self.device)
            
            # Inference
            with torch.no_grad():
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs[0]
                probs = torch.softmax(logits, dim=-1)
                predicted_class = torch.argmax(logits, dim=-1)
            
            # Convert to numpy
            probs = probs.cpu().numpy()[0]
            predicted_class = predicted_class.cpu().numpy()[0]
            
            # Decode label if encoder available
            if self.label_encoder is not None:
                predicted_label = self.label_encoder.inverse_transform([predicted_class])[0]
            else:
                predicted_label = f"class_{predicted_class}"
            
            result = {
                "predicted_class": int(predicted_class),
                "predicted_label": predicted_label,
                "confidence": float(probs[predicted_class])
            }
            
            if return_probs:
                result["probabilities"] = probs.tolist()
            
            return result
            
        except Exception as e:
            print(f"❌ Error during prediction: {e}")
            return {"error": str(e)}
    
    def predict_batch(self, texts: List[str], return_probs: bool = False) -> List[Dict[str, Any]]:
        """Predict for multiple documents"""
        results = []
        for text in texts:
            result = self.predict(text, return_probs)
            results.append(result)
        return results
    
    def save_model(self, output_dir: Path = None, model_name: str = "model"):
        """Save the trained model"""
        if self.model is None:
            print("❌ No model to save")
            return False
        
        try:
            output_dir = output_dir or self.model_dir
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save model weights
            model_path = output_dir / f"{model_name}.safetensors"
            from safetensors.torch import save_file
            save_file(self.model.state_dict(), model_path)
            
            # Save configuration
            config = {
                "model_name": self.model_name,
                "num_labels": self.model.num_labels,
                "dropout": self.model.dropout,
                "hidden_size": self.model.transformer.config.hidden_size
            }
            
            config_path = output_dir / "config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Save tokenizer
            if self.tokenizer:
                self.tokenizer.save_pretrained(output_dir)
            
            print(f"✅ Model saved to {output_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving model: {e}")
            return False

def load_model_for_inference(model_dir: str = None) -> ModelManager:
    """Convenience function to load model for inference"""
    manager = ModelManager()
    if manager.load_model(model_dir):
        return manager
    else:
        raise RuntimeError("Failed to load model")

if __name__ == "__main__":
    # Test model loading
    print("🧪 Testing model module...")
    
    try:
        manager = ModelManager()
        if manager.load_model():
            print("✅ Model loaded successfully!")
            
            # Test prediction
            test_text = "This is a test document for verification."
            result = manager.predict(test_text)
            print(f"Prediction result: {result}")
        else:
            print("❌ Model loading failed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("✅ Model module test completed!")
