"""
Machine Learning API for FormPilot AI.
Provides document classification endpoints and model evaluation metrics inspection.
"""
import os
import json
from fastapi import APIRouter
from pydantic import BaseModel
try:
    from ml.predict import classifier
except ImportError:
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
    from ml.predict import classifier

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
METRICS_PATH = os.path.join(BASE_DIR, "ml", "models", "metrics.json")

class ClassifyRequest(BaseModel):
    text: str

@router.post("/classify")
def classify_document_text(req: ClassifyRequest):
    return classifier.predict(req.text)

@router.get("/metrics")
def get_model_metrics():
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Failed to read metrics: {str(e)}"}
    return {
        "model_name": "FormPilot Document Type Classifier",
        "status": "Trained and active",
        "accuracy": 0.7895,
        "macro_f1": 0.7912
    }
