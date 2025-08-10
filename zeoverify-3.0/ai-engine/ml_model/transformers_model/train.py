"""
Training script for Zeoverify Document Verification Model
Handles model training, validation, and checkpointing
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformers import (
    AutoTokenizer, 
    AutoModel,
    get_linear_schedule_with_warmup,
    get_cosine_schedule_with_warmup
)
import numpy as np
import pandas as pd
from pathlib import Path
import json
import logging
from tqdm import tqdm
import argparse
from typing import Dict, Any, Optional, Tuple
import os

from ..config import TRAINING_CONFIG, MODEL_CONFIG
from ..preprocessing import DatasetPreprocessor
from .model import DocumentVerificationModel, ModelManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DocumentDataset(Dataset):
    """Custom dataset for document verification"""
    
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts.iloc[idx])
        label = self.labels.iloc[idx]
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

class Trainer:
    """Model trainer for document verification"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or TRAINING_CONFIG
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None
        self.optimizer = None
        self.scheduler = None
        self.criterion = nn.CrossEntropyLoss()
        
        logger.info(f"🖥️  Using device: {self.device}")
    
    def setup_model(self, model_name: str = None, num_labels: int = 2):
        """Setup model and tokenizer"""
        model_name = model_name or MODEL_CONFIG["model_name"]
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Initialize model
        self.model = DocumentVerificationModel(
            model_name=model_name,
            num_labels=num_labels
        )
        self.model.to(self.device)
        
        logger.info(f"✅ Model setup complete: {model_name}")
        logger.info(f"📊 Model parameters: {sum(p.numel() for p in self.model.parameters()):,}")
    
    def setup_optimizer(self, learning_rate: float = None):
        """Setup optimizer and scheduler"""
        learning_rate = learning_rate or MODEL_CONFIG["learning_rate"]
        
        # Optimizer
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=learning_rate,
            weight_decay=MODEL_CONFIG["weight_decay"]
        )
        
        # Scheduler
        total_steps = self.config["num_train_epochs"] * self.config["per_device_train_batch_size"]
        warmup_steps = self.config["warmup_steps"]
        
        self.scheduler = get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=warmup_steps,
            num_training_steps=total_steps
        )
        
        logger.info(f"✅ Optimizer setup complete: lr={learning_rate}, warmup_steps={warmup_steps}")
    
    def prepare_data(self, dataset_path: str, text_column: str, label_column: str):
        """Prepare training and validation data"""
        # Load and preprocess dataset
        preprocessor = DatasetPreprocessor()
        df = preprocessor.load_dataset(dataset_path)
        
        if df.empty:
            raise ValueError("Failed to load dataset")
        
        # Preprocess
        processed_data = preprocessor.preprocess_dataset(df, text_column, label_column)
        
        # Create datasets
        train_dataset = DocumentDataset(
            processed_data["train"][text_column],
            processed_data["train"][f"{label_column}_encoded"],
            self.tokenizer,
            max_length=MODEL_CONFIG["max_length"]
        )
        
        val_dataset = DocumentDataset(
            processed_data["test"][text_column],
            processed_data["test"][f"{label_column}_encoded"],
            self.tokenizer,
            max_length=MODEL_CONFIG["max_length"]
        )
        
        # Create dataloaders
        train_loader = DataLoader(
            train_dataset,
            batch_size=self.config["per_device_train_batch_size"],
            shuffle=True,
            num_workers=0
        )
        
        val_loader = DataLoader(
            val_dataset,
            batch_size=self.config["per_device_eval_batch_size"],
            shuffle=False,
            num_workers=0
        )
        
        logger.info(f"✅ Data prepared: {len(train_dataset)} train, {len(val_dataset)} val samples")
        
        return train_loader, val_loader, processed_data["label_encoder"]
    
    def train_epoch(self, train_loader: DataLoader) -> Dict[str, float]:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0
        correct_predictions = 0
        total_predictions = 0
        
        progress_bar = tqdm(train_loader, desc="Training")
        
        for batch in progress_bar:
            # Move to device
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            labels = batch['labels'].to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs[0]
            
            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()
            self.scheduler.step()
            
            # Statistics
            total_loss += loss.item()
            logits = outputs[1]
            preds = torch.argmax(logits, dim=-1)
            correct_predictions += (preds == labels).sum().item()
            total_predictions += labels.size(0)
            
            # Update progress bar
            progress_bar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{correct_predictions/total_predictions:.4f}'
            })
        
        epoch_loss = total_loss / len(train_loader)
        epoch_acc = correct_predictions / total_predictions
        
        return {'loss': epoch_loss, 'accuracy': epoch_acc}
    
    def validate(self, val_loader: DataLoader) -> Dict[str, float]:
        """Validate the model"""
        self.model.eval()
        total_loss = 0
        correct_predictions = 0
        total_predictions = 0
        
        with torch.no_grad():
            for batch in tqdm(val_loader, desc="Validation"):
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs[0]
                
                total_loss += loss.item()
                logits = outputs[1]
                preds = torch.argmax(logits, dim=-1)
                correct_predictions += (preds == labels).sum().item()
                total_predictions += labels.size(0)
        
        val_loss = total_loss / len(val_loader)
        val_acc = correct_predictions / total_predictions
        
        return {'loss': val_loss, 'accuracy': val_acc}
    
    def save_checkpoint(self, epoch: int, metrics: Dict[str, float], output_dir: Path):
        """Save training checkpoint"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'metrics': metrics,
            'config': self.config
        }
        
        checkpoint_path = output_dir / f"checkpoint-{epoch}.pt"
        torch.save(checkpoint, checkpoint_path)
        
        # Save best model
        if metrics.get('val_accuracy', 0) > getattr(self, 'best_val_acc', 0):
            self.best_val_acc = metrics['val_accuracy']
            best_model_path = output_dir / "best_model.pt"
            torch.save(self.model.state_dict(), best_model_path)
            logger.info(f"✅ New best model saved with val_acc: {self.best_val_acc:.4f}")
        
        logger.info(f"✅ Checkpoint saved: {checkpoint_path}")
    
    def train(self, dataset_path: str, text_column: str, label_column: str, 
              output_dir: str = None, num_epochs: int = None):
        """Main training loop"""
        num_epochs = num_epochs or self.config["num_train_epochs"]
        output_dir = Path(output_dir or self.config["output_dir"])
        
        logger.info("🚀 Starting training...")
        
        # Setup data
        train_loader, val_loader, label_encoder = self.prepare_data(
            dataset_path, text_column, label_column
        )
        
        # Training loop
        best_val_acc = 0
        for epoch in range(num_epochs):
            logger.info(f"\n📅 Epoch {epoch + 1}/{num_epochs}")
            
            # Train
            train_metrics = self.train_epoch(train_loader)
            logger.info(f"📚 Train - Loss: {train_metrics['loss']:.4f}, Acc: {train_metrics['accuracy']:.4f}")
            
            # Validate
            val_metrics = self.validate(val_loader)
            logger.info(f"🔍 Val - Loss: {val_metrics['loss']:.4f}, Acc: {val_metrics['accuracy']:.4f}")
            
            # Save checkpoint
            metrics = {**train_metrics, **{'val_' + k: v for k, v in val_metrics.items()}}
            self.save_checkpoint(epoch + 1, metrics, output_dir)
            
            # Update best accuracy
            if val_metrics['accuracy'] > best_val_acc:
                best_val_acc = val_metrics['accuracy']
                logger.info(f"🏆 New best validation accuracy: {best_val_acc:.4f}")
        
        # Save final model
        final_model_path = output_dir / "final_model.pt"
        torch.save(self.model.state_dict(), final_model_path)
        logger.info(f"✅ Training complete! Final model saved to {final_model_path}")
        
        return best_val_acc

def main():
    """Main training function"""
    parser = argparse.ArgumentParser(description="Train Zeoverify Document Verification Model")
    parser.add_argument("--dataset", required=True, help="Path to dataset CSV")
    parser.add_argument("--text_column", required=True, help="Name of text column")
    parser.add_argument("--label_column", required=True, help="Name of label column")
    parser.add_argument("--output_dir", default="./results", help="Output directory")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--learning_rate", type=float, default=2e-5, help="Learning rate")
    
    args = parser.parse_args()
    
    # Initialize trainer
    trainer = Trainer()
    
    # Setup model
    trainer.setup_model(num_labels=2)  # Assuming binary classification
    trainer.setup_optimizer(learning_rate=args.learning_rate)
    
    # Start training
    try:
        best_acc = trainer.train(
            dataset_path=args.dataset,
            text_column=args.text_column,
            label_column=args.label_column,
            output_dir=args.output_dir,
            num_epochs=args.epochs
        )
        print(f"🎉 Training completed! Best validation accuracy: {best_acc:.4f}")
        
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        raise

if __name__ == "__main__":
    main()
