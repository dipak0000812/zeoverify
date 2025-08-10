# 🤖 Zeoverify ML Model Package

This package contains the machine learning components for document verification in the Zeoverify system. It provides transformer-based models for detecting fraudulent documents with high accuracy.

## 📁 Package Structure

```
ml_model/
├── __init__.py                 # Package initialization
├── config.py                   # Configuration settings
├── preprocessing.py            # Data preprocessing utilities
├── requirements.txt            # Python dependencies
├── dataset/                    # Dataset management
│   ├── raw/                   # Raw data files
│   ├── processed/             # Preprocessed data
│   └── dataset.csv            # Main labeled dataset
├── transformers_model/         # Transformer-based model
│   ├── __init__.py            # Subpackage initialization
│   ├── model.py               # Model architecture & loading
│   ├── train.py               # Training script
│   ├── evaluate.py            # Model evaluation
│   └── model_weights/         # Saved model checkpoints
├── saved_model/                # Saved trained models
└── tests/                      # Unit tests
```

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements.txt[dev]
```

### 2. Basic Usage

```python
from ml_model import load_model_for_inference

# Load trained model
model_manager = load_model_for_inference("./saved_model")

# Verify document
result = model_manager.predict("This is a document to verify")
print(f"Prediction: {result['predicted_label']}")
print(f"Confidence: {result['confidence']:.2f}")
```

### 3. Training a New Model

```bash
# Train model with custom dataset
python -m ml_model.transformers_model.train \
    --dataset ./dataset/dataset.csv \
    --text_column text \
    --label_column label \
    --output_dir ./results \
    --epochs 10
```

### 4. Evaluating Model Performance

```bash
# Evaluate trained model
python -m ml_model.transformers_model.evaluate \
    --model ./saved_model/model.safetensors \
    --dataset ./dataset/test.csv \
    --text_column text \
    --label_column label \
    --output_dir ./evaluation_results
```

## 🔧 Configuration

The package uses a centralized configuration system in `config.py`:

- **MODEL_CONFIG**: Model architecture and hyperparameters
- **TRAINING_CONFIG**: Training settings and optimization
- **PREPROCESSING_CONFIG**: Data preprocessing options
- **API_CONFIG**: API service configuration

## 📊 Model Architecture

### DocumentVerificationModel

A transformer-based model that combines:
- Pre-trained transformer encoder (BERT/RoBERTa)
- Custom classification head
- Dropout regularization
- Xavier weight initialization

### Key Features

- **Multi-class support**: Configurable number of output classes
- **GPU acceleration**: Automatic CUDA detection and usage
- **Model checkpointing**: Save/load training progress
- **Flexible tokenization**: Support for various transformer tokenizers

## 🧹 Data Preprocessing

### TextPreprocessor

Handles text cleaning and normalization:
- Remove special characters and punctuation
- Convert to lowercase
- Normalize whitespace
- Handle encoding issues

### DatasetPreprocessor

Manages dataset operations:
- Load CSV/JSON datasets
- Split into train/validation sets
- Encode categorical labels
- Create PyTorch DataLoaders

## 🎯 Training Pipeline

### Trainer Class

Complete training workflow:
- Model and optimizer setup
- Data loading and batching
- Training and validation loops
- Checkpoint saving
- Progress monitoring

### Training Features

- **Learning rate scheduling**: Linear warmup with cosine decay
- **Gradient clipping**: Prevent exploding gradients
- **Early stopping**: Stop training when validation performance plateaus
- **Model checkpointing**: Save best model based on validation metrics

## 📈 Evaluation & Metrics

### Comprehensive Metrics

- **Classification metrics**: Accuracy, Precision, Recall, F1-Score
- **Per-class performance**: Individual class metrics
- **Confusion matrix**: Visual error analysis
- **ROC curves**: For binary classification
- **Precision-Recall curves**: Better for imbalanced datasets

### Visualization

- Confusion matrix heatmaps
- ROC and PR curves
- Training progress plots
- Performance comparison charts

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_model.py

# Run with coverage
python -m pytest tests/ --cov=ml_model --cov-report=html
```

## 📝 API Integration

The ML model integrates with the Zeoverify API:

```python
from ml_model import ModelManager

# Load model for API service
model_manager = ModelManager("./saved_model")
model_manager.load_model()

# API endpoint integration
@app.post("/verify")
async def verify_document(document_text: str):
    result = model_manager.predict(document_text)
    return {
        "status": "success",
        "verification_result": result
    }
```

## 🔍 Model Interpretability

### Confidence Scores

Each prediction includes confidence scores:
- **High confidence (>0.9)**: Very reliable prediction
- **Medium confidence (0.7-0.9)**: Reliable prediction
- **Low confidence (<0.7)**: Uncertain prediction

### Feature Importance

Analyze which parts of the document contribute to the prediction:
- Token-level attention weights
- Document segment analysis
- Key phrase identification

## 🚀 Performance Optimization

### Inference Optimization

- **Batch processing**: Process multiple documents simultaneously
- **Model quantization**: Reduce model size for faster inference
- **TensorRT integration**: GPU acceleration for production
- **Caching**: Cache tokenized inputs for repeated documents

### Training Optimization

- **Mixed precision**: Use FP16 for faster training
- **Gradient accumulation**: Handle large batch sizes
- **Distributed training**: Multi-GPU training support
- **Data parallelism**: Scale across multiple machines

## 📚 Examples

### Custom Training

```python
from ml_model.transformers_model import Trainer

# Initialize trainer
trainer = Trainer()

# Setup model and data
trainer.setup_model(num_labels=3)  # 3 classes
trainer.setup_optimizer(learning_rate=1e-5)

# Train model
best_acc = trainer.train(
    dataset_path="./data/documents.csv",
    text_column="content",
    label_column="authenticity",
    output_dir="./models",
    num_epochs=15
)
```

### Model Evaluation

```python
from ml_model.transformers_model import evaluate_model

# Evaluate model
results, report_file = evaluate_model(
    model_path="./models/best_model.pt",
    dataset_path="./data/test.csv",
    text_column="content",
    label_column="authenticity",
    output_dir="./evaluation"
)

print(f"Best accuracy: {results['metrics']['overall']['accuracy']:.4f}")
```

## 🐛 Troubleshooting

### Common Issues

1. **CUDA out of memory**: Reduce batch size or use gradient accumulation
2. **Model loading errors**: Check model file paths and compatibility
3. **Training instability**: Adjust learning rate and warmup steps
4. **Poor performance**: Check data quality and preprocessing

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the test examples
- Contact the development team

---

**Note**: This package requires Python 3.8+ and PyTorch 2.0+. For GPU acceleration, ensure CUDA compatibility.
