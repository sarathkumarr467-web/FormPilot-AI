"""
Evaluation script for FormPilot AI Document Classification Model.
Loads test data or cross-validation metrics and displays formatted performance report.
"""
import os
import json
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
METRICS_PATH = os.path.join(BASE_DIR, "models", "metrics.json")
MODEL_PATH = os.path.join(BASE_DIR, "models", "document_classifier.joblib")

def evaluate():
    if not os.path.exists(METRICS_PATH):
        print("Metrics file not found. Please run train.py first.")
        return
        
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)
        
    print("\n" + "=" * 65)
    print("  FORMPILOT AI — Model Evaluation Summary")
    print("=" * 65)
    print(f"Model Architecture : {metrics['architecture']}")
    print(f"Dataset Size       : {metrics['total_samples']} annotated documents")
    print(f"Overall Accuracy   : {metrics['accuracy'] * 100:.2f}%")
    print(f"Macro F1-Score     : {metrics['macro_f1']:.4f}")
    print("-" * 65)
    print(f"{'Class Label':24s} | {'Precision':10s} | {'Recall':10s} | {'F1-Score':10s} | {'Samples':7s}")
    print("-" * 65)
    for c in metrics["classes"]:
        r = metrics["classification_report"][c]
        print(f"{c:24s} | {r['precision']:10.3f} | {r['recall']:10.3f} | {r['f1-score']:10.3f} | {int(r['support']):7d}")
    print("-" * 65)
    print("\nConfusion Matrix:")
    labels = metrics["labels_order"]
    header = "       " + " ".join([f"{l[:6]:>7}" for l in labels])
    print(header)
    for i, row in enumerate(metrics["confusion_matrix"]):
        row_str = " ".join([f"{val:>7}" for val in row])
        print(f"{labels[i][:6]:>6}: {row_str}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    evaluate()
