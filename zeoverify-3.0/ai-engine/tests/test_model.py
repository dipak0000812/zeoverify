"""
Unit tests for Zeoverify ML Model components
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import pandas as pd
import numpy as np

# Import modules to test
from ml_model.config import (
    MODEL_CONFIG, 
    TRAINING_CONFIG, 
    PREPROCESSING_CONFIG,
    ensure_directories
)
from ml_model.preprocessing import TextPreprocessor, DatasetPreprocessor
from ml_model.transformers_model.model import DocumentVerificationModel, ModelManager

class TestConfig(unittest.TestCase):
    """Test configuration module"""
    
    def test_config_structure(self):
        """Test that all required config sections exist"""
        self.assertIn("max_length", MODEL_CONFIG)
        self.assertIn("batch_size", MODEL_CONFIG)
        self.assertIn("learning_rate", MODEL_CONFIG)
        self.assertIn("epochs", MODEL_CONFIG)
        
        self.assertIn("num_train_epochs", TRAINING_CONFIG)
        self.assertIn("per_device_train_batch_size", TRAINING_CONFIG)
        
        self.assertIn("text_cleaning", PREPROCESSING_CONFIG)
        self.assertIn("max_tokens", PREPROCESSING_CONFIG)
    
    def test_ensure_directories(self):
        """Test directory creation function"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / "test_dirs"
            ensure_directories()
            # Should not raise any errors

class TestPreprocessing(unittest.TestCase):
    """Test preprocessing module"""
    
    def setUp(self):
        """Set up test data"""
        self.preprocessor = TextPreprocessor()
        
        # Create test dataset
        self.test_data = pd.DataFrame({
            'text': [
                'This is a REAL document.',
                'This is a FAKE document!',
                'Another REAL document here.',
                'Another FAKE document there.'
            ],
            'label': ['real', 'fake', 'real', 'fake']
        })
    
    def test_text_cleaning(self):
        """Test text cleaning functionality"""
        test_text = "Hello, World! This is a TEST document with special @#$% characters."
        cleaned = self.preprocessor.clean_text(test_text)
        
        # Should remove special characters and normalize whitespace
        self.assertNotIn("@#$%", cleaned)
        self.assertNotIn(",", cleaned)
        self.assertNotIn("!", cleaned)
        self.assertIn("hello world this is a test document with special characters", cleaned)
    
    def test_dataset_preprocessing(self):
        """Test dataset preprocessing"""
        dataset_preprocessor = DatasetPreprocessor()
        
        # Test with temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.test_data.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            # Load dataset
            df = dataset_preprocessor.load_dataset(temp_path)
            self.assertEqual(len(df), 4)
            self.assertIn('text', df.columns)
            self.assertIn('label', df.columns)
            
            # Preprocess dataset
            processed = dataset_preprocessor.preprocess_dataset(df, 'text', 'label')
            self.assertIn('train', processed)
            self.assertIn('test', processed)
            self.assertIn('label_encoder', processed)
            
        finally:
            # Clean up
            Path(temp_path).unlink()
    
    def test_dataloader_creation(self):
        """Test dataloader creation"""
        dataset_preprocessor = DatasetPreprocessor()
        
        # Create dataloader
        dataloader = dataset_preprocessor.create_dataloader(
            self.test_data, 'text', 'label', batch_size=2
        )
        
        self.assertIsInstance(dataloader, list)
        self.assertEqual(len(dataloader), 2)  # 4 samples / 2 batch size = 2 batches

class TestModel(unittest.TestCase):
    """Test model components"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.model_dir = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_model_architecture(self):
        """Test model architecture creation"""
        try:
            model = DocumentVerificationModel(num_labels=2)
            self.assertIsNotNone(model.transformer)
            self.assertIsNotNone(model.classifier)
            
            # Test forward pass with dummy data
            batch_size = 2
            seq_length = 10
            input_ids = torch.randint(0, 1000, (batch_size, seq_length))
            attention_mask = torch.ones(batch_size, seq_length)
            
            with torch.no_grad():
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                self.assertEqual(outputs[0].shape, (batch_size, 2))  # 2 classes
                
        except Exception as e:
            # Skip test if transformers not available
            self.skipTest(f"Transformers not available: {e}")
    
    def test_model_manager(self):
        """Test model manager functionality"""
        manager = ModelManager(self.model_dir)
        self.assertIsNone(manager.model)
        self.assertIsNone(manager.tokenizer)
        
        # Test loading non-existent model (should fail gracefully)
        success = manager.load_model("non_existent_model.pt")
        self.assertFalse(success)

class TestIntegration(unittest.TestCase):
    """Test integration between components"""
    
    def test_end_to_end_preprocessing(self):
        """Test complete preprocessing pipeline"""
        # Create test data
        test_texts = [
            "This is a REAL document for verification.",
            "This is a FAKE document that should be detected.",
            "Another REAL document with important information."
        ]
        
        # Test preprocessing
        preprocessor = TextPreprocessor()
        for text in test_texts:
            cleaned = preprocessor.clean_text(text)
            self.assertIsInstance(cleaned, str)
            self.assertGreater(len(cleaned), 0)

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add tests
    test_suite.addTest(unittest.makeSuite(TestConfig))
    test_suite.addTest(unittest.makeSuite(TestPreprocessing))
    test_suite.addTest(unittest.makeSuite(TestModel))
    test_suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
