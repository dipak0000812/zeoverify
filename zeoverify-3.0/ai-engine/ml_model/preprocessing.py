"""
Data preprocessing module for Zeoverify ML Model
Handles text cleaning, tokenization, and data preparation
"""

import re
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path
import pickle
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from .config import PREPROCESSING_CONFIG, MODEL_CONFIG

class TextPreprocessor:
    """Text preprocessing and cleaning utilities"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or PREPROCESSING_CONFIG
        self.tokenizer = None
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not isinstance(text, str):
            return ""
            
        # Convert to lowercase if configured
        if self.config.get("lowercase", True):
            text = text.lower()
            
        # Remove special characters if configured
        if self.config.get("remove_special_chars", True):
            text = re.sub(r'[^\w\s]', '', text)
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_text(self, text: str, max_length: int = None) -> Dict[str, Any]:
        """Tokenize text using the configured tokenizer"""
        if not self.tokenizer:
            self._load_tokenizer()
            
        max_length = max_length or self.config.get("max_tokens", 512)
        
        # Clean text first
        cleaned_text = self.clean_text(text)
        
        # Tokenize
        encoding = self.tokenizer(
            cleaned_text,
            truncation=self.config.get("truncation", True),
            padding=self.config.get("padding", "max_length"),
            max_length=max_length,
            return_tensors="pt"
        )
        
        return {
            "input_ids": encoding["input_ids"],
            "attention_mask": encoding["attention_mask"],
            "token_type_ids": encoding.get("token_type_ids")
        }
    
    def _load_tokenizer(self):
        """Load the tokenizer from saved model or default"""
        try:
            # Try to load from saved model first
            from .config import SAVED_TOKENIZER_PATH
            if SAVED_TOKENIZER_PATH.exists():
                self.tokenizer = AutoTokenizer.from_pretrained(str(SAVED_TOKENIZER_PATH))
            else:
                # Fall back to default model
                self.tokenizer = AutoTokenizer.from_pretrained(MODEL_CONFIG["model_name"])
        except Exception as e:
            print(f"Warning: Could not load tokenizer: {e}")
            # Use default tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_CONFIG["model_name"])

class DatasetPreprocessor:
    """Dataset preprocessing and preparation"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or PREPROCESSING_CONFIG
        self.text_preprocessor = TextPreprocessor(config)
        self.label_encoder = LabelEncoder()
        
    def load_dataset(self, dataset_path: str) -> pd.DataFrame:
        """Load dataset from CSV or other format"""
        try:
            if dataset_path.endswith('.csv'):
                df = pd.read_csv(dataset_path)
            else:
                raise ValueError(f"Unsupported dataset format: {dataset_path}")
                
            print(f"✅ Dataset loaded: {len(df)} samples")
            return df
            
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return pd.DataFrame()
    
    def preprocess_dataset(self, df: pd.DataFrame, text_column: str, label_column: str) -> Dict[str, Any]:
        """Preprocess entire dataset"""
        if df.empty:
            return {}
            
        print("🔄 Preprocessing dataset...")
        
        # Clean text data
        df[f"{text_column}_cleaned"] = df[text_column].apply(
            self.text_preprocessor.clean_text
        )
        
        # Encode labels
        if label_column in df.columns:
            labels = df[label_column].values
            encoded_labels = self.label_encoder.fit_transform(labels)
            df[f"{label_column}_encoded"] = encoded_labels
            
            # Save label encoder
            self._save_label_encoder()
        
        # Split dataset
        train_df, test_df = train_test_split(
            df, test_size=0.2, random_state=42, stratify=df.get(f"{label_column}_encoded", None)
        )
        
        print(f"✅ Dataset preprocessed: {len(train_df)} train, {len(test_df)} test samples")
        
        return {
            "train": train_df,
            "test": test_df,
            "label_encoder": self.label_encoder
        }
    
    def _save_label_encoder(self):
        """Save the fitted label encoder"""
        try:
            from .config import SAVED_MODEL_DIR
            encoder_path = SAVED_MODEL_DIR / "label_encoder.pkl"
            with open(encoder_path, 'wb') as f:
                pickle.dump(self.label_encoder, f)
            print(f"✅ Label encoder saved to {encoder_path}")
        except Exception as e:
            print(f"❌ Error saving label encoder: {e}")
    
    def create_dataloader(self, df: pd.DataFrame, text_column: str, label_column: str = None, 
                         batch_size: int = 16) -> List[Dict[str, Any]]:
        """Create dataloader for training"""
        dataloader = []
        
        for i in range(0, len(df), batch_size):
            batch_df = df.iloc[i:i+batch_size]
            batch_data = []
            
            for _, row in batch_df.iterrows():
                text = row[text_column]
                tokenized = self.text_preprocessor.tokenize_text(text)
                
                sample = {
                    "input_ids": tokenized["input_ids"],
                    "attention_mask": tokenized["attention_mask"]
                }
                
                if label_column and f"{label_column}_encoded" in row:
                    sample["labels"] = torch.tensor([row[f"{label_column}_encoded"]])
                
                batch_data.append(sample)
            
            dataloader.append(batch_data)
        
        return dataloader

def preprocess_single_document(text: str, max_length: int = 512) -> Dict[str, Any]:
    """Preprocess a single document for inference"""
    preprocessor = TextPreprocessor()
    return preprocessor.tokenize_text(text, max_length)

def load_and_preprocess_dataset(dataset_path: str, text_column: str, label_column: str) -> Dict[str, Any]:
    """Convenience function to load and preprocess dataset"""
    dataset_preprocessor = DatasetPreprocessor()
    
    # Load dataset
    df = dataset_preprocessor.load_dataset(dataset_path)
    if df.empty:
        return {}
    
    # Preprocess dataset
    processed_data = dataset_preprocessor.preprocess_dataset(df, text_column, label_column)
    
    return processed_data

if __name__ == "__main__":
    # Test preprocessing
    print("🧪 Testing preprocessing module...")
    
    # Test text cleaning
    preprocessor = TextPreprocessor()
    test_text = "Hello, World! This is a TEST document with special @#$% characters."
    cleaned = preprocessor.clean_text(test_text)
    print(f"Original: {test_text}")
    print(f"Cleaned: {cleaned}")
    
    print("✅ Preprocessing module test completed!")
