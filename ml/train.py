"""
Training pipeline for FormPilot AI Document Classification Model.
Trains a TF-IDF + Calibrated Linear Support Vector Classifier on application documents.
"""
import os
import json
import joblib
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

from preprocess import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "dataset.json")
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_OUTPUT_PATH = os.path.join(MODELS_DIR, "document_classifier.joblib")
METRICS_OUTPUT_PATH = os.path.join(MODELS_DIR, "metrics.json")

def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    texts = [item["text"] for item in data]
    labels = [item["category"] for item in data]
    return texts, labels

def train():
    print("=" * 65)
    print("  FORMPILOT AI — Document Type Classifier Training")
    print("=" * 65)
    
    texts, labels = load_dataset()
    print(f"Loaded {len(texts)} samples across {len(set(labels))} classes: {sorted(list(set(labels)))}")
    
    cleaned_texts = [clean_text(t) for t in texts]
    
    # Define Pipeline with TF-IDF and Calibrated LinearSVC (to provide predict_proba)
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=2500,
            sublinear_tf=True
        )),
        ("clf", CalibratedClassifierCV(
            estimator=LinearSVC(C=1.0, random_state=42, max_iter=2000),
            cv=3
        ))
    ])
    
    # Perform Stratified K-Fold Cross-Validation evaluation
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    y_pred = cross_val_predict(pipeline, cleaned_texts, labels, cv=skf)
    
    unique_labels = sorted(list(set(labels)))
    report = classification_report(labels, y_pred, labels=unique_labels, output_dict=True, zero_division=0)
    cm = confusion_matrix(labels, y_pred, labels=unique_labels).tolist()
    acc = accuracy_score(labels, y_pred)
    macro_f1 = f1_score(labels, y_pred, average="macro")
    
    print("\n--- Cross-Validation Evaluation Results ---")
    print(f"Overall Accuracy: {acc * 100:.2f}%")
    print(f"Macro F1-Score:   {macro_f1:.4f}")
    print("\nDetailed Per-Class Metrics:")
    for label in unique_labels:
        p = report[label]["precision"]
        r = report[label]["recall"]
        f = report[label]["f1-score"]
        s = report[label]["support"]
        print(f"  * {label:24s} | P: {p:.3f} | R: {r:.3f} | F1: {f:.3f} | N: {s}")
        
    # Fit final pipeline on all training data
    pipeline.fit(cleaned_texts, labels)
    
    # Save model and metadata
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(pipeline, MODEL_OUTPUT_PATH)
    print(f"\nModel saved successfully -> {MODEL_OUTPUT_PATH}")
    
    metrics_data = {
        "model_name": "FormPilot Document Type Classifier",
        "architecture": "TF-IDF (1-2 ngrams) + Calibrated LinearSVC",
        "total_samples": len(texts),
        "classes": unique_labels,
        "accuracy": round(float(acc), 4),
        "macro_f1": round(float(macro_f1), 4),
        "classification_report": report,
        "confusion_matrix": cm,
        "labels_order": unique_labels
    }
    with open(METRICS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=2)
    print(f"Metrics saved successfully -> {METRICS_OUTPUT_PATH}")
    print("=" * 65)

if __name__ == "__main__":
    train()
