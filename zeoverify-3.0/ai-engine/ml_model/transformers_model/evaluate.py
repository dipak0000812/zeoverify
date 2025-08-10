"""
Model evaluation script for Zeoverify Document Verification
Handles model evaluation, metrics calculation, and performance analysis
"""

import torch
import numpy as np
import pandas as pd
from pathlib import Path
import json
import logging
from typing import Dict, Any, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    roc_curve, 
    auc,
    precision_recall_curve,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
import argparse
from tqdm import tqdm

from ..config import MODEL_CONFIG
from ..preprocessing import DatasetPreprocessor
from .model import ModelManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """Evaluates trained model performance"""
    
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.device = model_manager.device
        self.results = {}
        
    def evaluate_dataset(self, dataset_path: str, text_column: str, label_column: str) -> Dict[str, Any]:
        """Evaluate model on entire dataset"""
        logger.info(f"🔍 Evaluating model on dataset: {dataset_path}")
        
        # Load and preprocess dataset
        preprocessor = DatasetPreprocessor()
        df = preprocessor.load_dataset(dataset_path)
        
        if df.empty:
            raise ValueError("Failed to load dataset")
        
        # Preprocess
        processed_data = preprocessor.preprocess_dataset(df, text_column, label_column)
        
        # Get predictions
        texts = processed_data["test"][text_column].tolist()
        true_labels = processed_data["test"][f"{label_column}_encoded"].tolist()
        
        predictions = []
        probabilities = []
        
        logger.info("📊 Running predictions...")
        for text in tqdm(texts, desc="Evaluating"):
            result = self.model_manager.predict(text, return_probs=True)
            if "error" not in result:
                predictions.append(result["predicted_class"])
                probabilities.append(result["probabilities"])
            else:
                logger.warning(f"Prediction failed: {result['error']}")
                predictions.append(-1)  # Invalid prediction
                probabilities.append([0.5, 0.5])  # Default probabilities
        
        # Calculate metrics
        metrics = self._calculate_metrics(true_labels, predictions, probabilities)
        
        # Save results
        self.results = {
            "dataset_path": dataset_path,
            "num_samples": len(texts),
            "metrics": metrics,
            "predictions": predictions,
            "true_labels": true_labels,
            "probabilities": probabilities
        }
        
        logger.info("✅ Evaluation completed!")
        return self.results
    
    def _calculate_metrics(self, true_labels: List[int], predictions: List[int], 
                          probabilities: List[List[float]]) -> Dict[str, Any]:
        """Calculate comprehensive evaluation metrics"""
        # Filter out invalid predictions
        valid_mask = [p != -1 for p in predictions]
        if not any(valid_mask):
            return {"error": "No valid predictions"}
        
        y_true = [true_labels[i] for i in range(len(true_labels)) if valid_mask[i]]
        y_pred = [predictions[i] for i in range(len(predictions)) if valid_mask[i]]
        y_probs = [probabilities[i] for i in range(len(probabilities)) if valid_mask[i]]
        
        # Basic metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted')
        recall = recall_score(y_true, y_pred, average='weighted')
        f1 = f1_score(y_true, y_pred, average='weighted')
        
        # Per-class metrics
        class_precision = precision_score(y_true, y_pred, average=None)
        class_recall = recall_score(y_true, y_pred, average=None)
        class_f1 = f1_score(y_true, y_pred, average=None)
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # ROC and AUC (for binary classification)
        roc_auc = None
        if len(set(y_true)) == 2:  # Binary classification
            try:
                # Get positive class probabilities
                pos_probs = [prob[1] if len(prob) > 1 else prob[0] for prob in y_probs]
                fpr, tpr, _ = roc_curve(y_true, pos_probs)
                roc_auc = auc(fpr, tpr)
            except Exception as e:
                logger.warning(f"Could not calculate ROC AUC: {e}")
        
        # Precision-Recall curve
        pr_auc = None
        if len(set(y_true)) == 2:  # Binary classification
            try:
                pos_probs = [prob[1] if len(prob) > 1 else prob[0] for prob in y_probs]
                precision_curve, recall_curve, _ = precision_recall_curve(y_true, pos_probs)
                pr_auc = auc(recall_curve, precision_curve)
            except Exception as e:
                logger.warning(f"Could not calculate PR AUC: {e}")
        
        metrics = {
            "overall": {
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
                "f1_score": float(f1)
            },
            "per_class": {
                "precision": class_precision.tolist() if class_precision is not None else [],
                "recall": class_recall.tolist() if class_recall is not None else [],
                "f1_score": class_f1.tolist() if class_f1 is not None else []
            },
            "confusion_matrix": cm.tolist(),
            "roc_auc": float(roc_auc) if roc_auc is not None else None,
            "pr_auc": float(pr_auc) if pr_auc is not None else None,
            "num_samples": len(y_true),
            "num_classes": len(set(y_true))
        }
        
        return metrics
    
    def generate_report(self, output_dir: Path = None) -> str:
        """Generate comprehensive evaluation report"""
        if not self.results:
            return "No evaluation results available"
        
        output_dir = output_dir or Path("./evaluation_results")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save results to JSON
        results_file = output_dir / "evaluation_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Generate classification report
        if "metrics" in self.results and "error" not in self.results["metrics"]:
            metrics = self.results["metrics"]
            
            # Print summary
            print("\n" + "="*60)
            print("📊 MODEL EVALUATION RESULTS")
            print("="*60)
            
            print(f"\n📁 Dataset: {self.results['dataset_path']}")
            print(f"📊 Total samples: {self.results['num_samples']}")
            print(f"🎯 Number of classes: {metrics['num_classes']}")
            
            print(f"\n🏆 OVERALL PERFORMANCE:")
            overall = metrics["overall"]
            print(f"   Accuracy:  {overall['accuracy']:.4f}")
            print(f"   Precision: {overall['precision']:.4f}")
            print(f"   Recall:    {overall['recall']:.4f}")
            print(f"   F1-Score:  {overall['f1_score']:.4f}")
            
            if metrics.get("roc_auc"):
                print(f"   ROC AUC:   {metrics['roc_auc']:.4f}")
            if metrics.get("pr_auc"):
                print(f"   PR AUC:    {metrics['pr_auc']:.4f}")
            
            # Per-class metrics
            if metrics["per_class"]["precision"]:
                print(f"\n📈 PER-CLASS PERFORMANCE:")
                for i, (prec, rec, f1) in enumerate(zip(
                    metrics["per_class"]["precision"],
                    metrics["per_class"]["recall"],
                    metrics["per_class"]["f1_score"]
                )):
                    print(f"   Class {i}: Precision={prec:.4f}, Recall={rec:.4f}, F1={f1:.4f}")
            
            # Confusion matrix
            print(f"\n🔍 CONFUSION MATRIX:")
            cm = np.array(metrics["confusion_matrix"])
            print(cm)
            
            # Save confusion matrix plot
            self._plot_confusion_matrix(cm, output_dir)
            
            # Save ROC curve if available
            if metrics.get("roc_auc") and "probabilities" in self.results:
                self._plot_roc_curve(output_dir)
            
            # Save precision-recall curve if available
            if metrics.get("pr_auc") and "probabilities" in self.results:
                self._plot_pr_curve(output_dir)
        
        print(f"\n💾 Detailed results saved to: {results_file}")
        return str(results_file)
    
    def _plot_confusion_matrix(self, cm: np.ndarray, output_dir: Path):
        """Plot and save confusion matrix"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Fake', 'Real'], 
                   yticklabels=['Fake', 'Real'])
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        
        cm_file = output_dir / "confusion_matrix.png"
        plt.savefig(cm_file, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"📊 Confusion matrix saved to: {cm_file}")
    
    def _plot_roc_curve(self, output_dir: Path):
        """Plot and save ROC curve"""
        if "probabilities" not in self.results:
            return
        
        y_true = self.results["true_labels"]
        y_probs = self.results["probabilities"]
        
        # Get positive class probabilities
        pos_probs = [prob[1] if len(prob) > 1 else prob[0] for prob in y_probs]
        
        fpr, tpr, _ = roc_curve(y_true, pos_probs)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.tight_layout()
        
        roc_file = output_dir / "roc_curve.png"
        plt.savefig(roc_file, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"📊 ROC curve saved to: {roc_file}")
    
    def _plot_pr_curve(self, output_dir: Path):
        """Plot and save Precision-Recall curve"""
        if "probabilities" not in self.results:
            return
        
        y_true = self.results["true_labels"]
        y_probs = self.results["probabilities"]
        
        # Get positive class probabilities
        pos_probs = [prob[1] if len(prob) > 1 else prob[0] for prob in y_probs]
        
        precision_curve, recall_curve, _ = precision_recall_curve(y_true, pos_probs)
        pr_auc = auc(recall_curve, precision_curve)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall_curve, precision_curve, color='blue', lw=2,
                label=f'PR curve (AUC = {pr_auc:.2f})')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.legend(loc="lower left")
        plt.grid(True)
        plt.tight_layout()
        
        pr_file = output_dir / "precision_recall_curve.png"
        plt.savefig(pr_file, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"📊 Precision-Recall curve saved to: {pr_file}")

def evaluate_model(model_path: str, dataset_path: str, text_column: str, 
                  label_column: str, output_dir: str = "./evaluation_results"):
    """Convenience function to evaluate a model"""
    
    # Load model
    logger.info(f"🔄 Loading model from: {model_path}")
    model_manager = ModelManager()
    
    if not model_manager.load_model(model_path):
        raise RuntimeError("Failed to load model")
    
    # Create evaluator
    evaluator = ModelEvaluator(model_manager)
    
    # Evaluate
    results = evaluator.evaluate_dataset(dataset_path, text_column, label_column)
    
    # Generate report
    report_file = evaluator.generate_report(Path(output_dir))
    
    return results, report_file

def main():
    """Main evaluation function"""
    parser = argparse.ArgumentParser(description="Evaluate Zeoverify Document Verification Model")
    parser.add_argument("--model", required=True, help="Path to trained model")
    parser.add_argument("--dataset", required=True, help="Path to evaluation dataset")
    parser.add_argument("--text_column", required=True, help="Name of text column")
    parser.add_argument("--label_column", required=True, help="Name of label column")
    parser.add_argument("--output_dir", default="./evaluation_results", help="Output directory")
    
    args = parser.parse_args()
    
    try:
        results, report_file = evaluate_model(
            model_path=args.model,
            dataset_path=args.dataset,
            text_column=args.text_column,
            label_column=args.label_column,
            output_dir=args.output_dir
        )
        
        print(f"\n🎉 Evaluation completed successfully!")
        print(f"📄 Report saved to: {report_file}")
        
    except Exception as e:
        logger.error(f"❌ Evaluation failed: {e}")
        raise

if __name__ == "__main__":
    main()
