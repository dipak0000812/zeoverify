"""
Configuration file for Zeoverify ML Model
Contains all paths, hyperparameters, and model settings
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
ML_MODEL_DIR = BASE_DIR / "ml_model"
DATASET_DIR = ML_MODEL_DIR / "dataset"
TRANSFORMERS_DIR = ML_MODEL_DIR / "transformers_model"
SAVED_MODEL_DIR = ML_MODEL_DIR / "saved_model"

# Dataset paths
RAW_DATA_DIR = DATASET_DIR / "raw"
PROCESSED_DATA_DIR = DATASET_DIR / "processed"
DATASET_CSV = DATASET_DIR / "dataset.csv"

# Model paths
MODEL_WEIGHTS_DIR = TRANSFORMERS_DIR / "model_weights"
TOKENIZER_PATH = TRANSFORMERS_DIR / "tokenizer.pkl"
CONFIG_PATH = TRANSFORMERS_DIR / "config.json"

# Saved model paths
SAVED_MODEL_PATH = SAVED_MODEL_DIR / "model.safetensors"
SAVED_CONFIG_PATH = SAVED_MODEL_DIR / "config.json"
SAVED_TOKENIZER_PATH = SAVED_MODEL_DIR / "tokenizer.json"

# Model hyperparameters
MODEL_CONFIG = {
    "max_length": 512,
    "batch_size": 16,
    "learning_rate": 2e-5,
    "epochs": 10,
    "warmup_steps": 500,
    "weight_decay": 0.01,
    "model_name": "bert-base-uncased"
}

# Training configuration
TRAINING_CONFIG = {
    "output_dir": str(TRANSFORMERS_DIR / "results"),
    "num_train_epochs": 10,
    "per_device_train_batch_size": 16,
    "per_device_eval_batch_size": 16,
    "warmup_steps": 500,
    "weight_decay": 0.01,
    "logging_dir": str(TRANSFORMERS_DIR / "logs"),
    "logging_steps": 10,
    "save_steps": 1000,
    "eval_steps": 1000,
    "save_total_limit": 3,
}

# Data preprocessing
PREPROCESSING_CONFIG = {
    "text_cleaning": True,
    "remove_special_chars": True,
    "lowercase": True,
    "max_tokens": 512,
    "padding": "max_length",
    "truncation": True
}

# API configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 5001,
    "debug": True,
    "max_file_size": 16 * 1024 * 1024,  # 16MB
    "allowed_extensions": [".pdf", ".jpg", ".jpeg", ".png", ".txt"]
}

# Ensure directories exist
def ensure_directories():
    """Create all required directories if they don't exist"""
    directories = [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        MODEL_WEIGHTS_DIR,
        SAVED_MODEL_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_directories()
    print("✅ All directories created successfully!")
