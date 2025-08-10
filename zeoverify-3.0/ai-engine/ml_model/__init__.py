"""
Zeoverify ML Model Package
Document verification using transformer-based models
"""

from .config import (
    MODEL_CONFIG,
    TRAINING_CONFIG,
    PREPROCESSING_CONFIG,
    API_CONFIG,
    ensure_directories
)

from .preprocessing import (
    TextPreprocessor,
    DatasetPreprocessor,
    preprocess_single_document,
    load_and_preprocess_dataset
)

from .transformers_model.model import (
    DocumentVerificationModel,
    ModelManager,
    load_model_for_inference
)

from .transformers_model.train import Trainer
from .transformers_model.evaluate import ModelEvaluator, evaluate_model

__version__ = "1.0.0"
__author__ = "Zeoverify Team"

__all__ = [
    # Configuration
    "MODEL_CONFIG",
    "TRAINING_CONFIG", 
    "PREPROCESSING_CONFIG",
    "API_CONFIG",
    "ensure_directories",
    
    # Preprocessing
    "TextPreprocessor",
    "DatasetPreprocessor",
    "preprocess_single_document",
    "load_and_preprocess_dataset",
    
    # Model
    "DocumentVerificationModel",
    "ModelManager",
    "load_model_for_inference",
    
    # Training
    "Trainer",
    
    # Evaluation
    "ModelEvaluator",
    "evaluate_model"
]
