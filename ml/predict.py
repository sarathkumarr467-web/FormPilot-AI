"""
Inference service for FormPilot AI Document Classification Model.
Takes document text and returns predicted category, confidence score, and distribution.
"""
import os
import joblib
from typing import Dict, Any
try:
    from .preprocess import clean_text, extract_keywords
except ImportError:
    from preprocess import clean_text, extract_keywords

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "document_classifier.joblib")

CATEGORY_FRIENDLY_NAMES = {
    "scholarship_form": {
        "en": "Scholarship Application Form",
        "ta": "கல்வி உதவித்தொகை விண்ணப்பப் படிவம்"
    },
    "college_admission": {
        "en": "College / University Admission Form",
        "ta": "கல்லூரி / பல்கலைக்கழக சேர்க்கை படிவம்"
    },
    "job_application": {
        "en": "Employment / Recruitment Job Application",
        "ta": "வேலைவாய்ப்பு / பணி நியமன விண்ணப்பம்"
    },
    "internship_application": {
        "en": "Internship / Research Training Application",
        "ta": "பயிற்சி / இன்டர்ன்ஷிப் விண்ணப்பப் படிவம்"
    },
    "government_scheme": {
        "en": "Government Welfare Scheme Application",
        "ta": "அரசு நலத்திட்ட விண்ணப்பப் படிவம்"
    },
    "supporting_document": {
        "en": "Identity / Academic Supporting Document",
        "ta": "அடையாள / கல்வி சான்றிதழ் ஆவணம்"
    }
}

class DocumentClassifier:
    _instance = None
    
    def __init__(self):
        self.model = None
        self.load_model()
        
    def load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
            except Exception as e:
                print(f"[DocumentClassifier] Warning: Could not load model: {e}")
                self.model = None
        else:
            self.model = None

    def predict(self, text: str) -> Dict[str, Any]:
        """Classify document text."""
        cleaned = clean_text(text)
        if not cleaned:
            return {
                "category": "unknown",
                "confidence": 0.0,
                "label_en": "Unknown Document",
                "label_ta": "தெரியாத ஆவணம்",
                "distribution": {},
                "keywords": []
            }
            
        if self.model is None:
            # Fallback heuristic classifier if model is not loaded yet
            return self._heuristic_fallback(cleaned)
            
        try:
            probabilities = self.model.predict_proba([cleaned])[0]
            classes = self.model.classes_
            top_idx = probabilities.argmax()
            top_class = classes[top_idx]
            top_conf = float(probabilities[top_idx])
            
            distribution = {
                cls_name: round(float(prob), 4)
                for cls_name, prob in zip(classes, probabilities)
            }
            
            friendly = CATEGORY_FRIENDLY_NAMES.get(top_class, {
                "en": top_class.replace("_", " ").title(),
                "ta": top_class
            })
            
            return {
                "category": top_class,
                "confidence": round(top_conf, 4),
                "label_en": friendly["en"],
                "label_ta": friendly["ta"],
                "distribution": distribution,
                "keywords": extract_keywords(cleaned, top_k=8)
            }
        except Exception as e:
            print(f"[DocumentClassifier] Prediction error: {e}")
            return self._heuristic_fallback(cleaned)
            
    def _heuristic_fallback(self, cleaned: str) -> Dict[str, Any]:
        """Deterministic keyword-based fallback if model is unpickled."""
        c = cleaned.lower()
        if "scholarship" in c or "fellowship" in c or "stipend" in c:
            cat = "scholarship_form"
        elif "admission" in c or "entrance" in c or "cutoff" in c or "degree" in c:
            cat = "college_admission"
        elif "recruitment" in c or "vacancy" in c or "post applied" in c or "salary" in c:
            cat = "job_application"
        elif "internship" in c or "trainee" in c or "apprentice" in c:
            cat = "internship_application"
        elif "scheme" in c or "yojana" in c or "beneficiary" in c or "subsidy" in c:
            cat = "government_scheme"
        else:
            cat = "supporting_document"
            
        friendly = CATEGORY_FRIENDLY_NAMES.get(cat, {"en": cat, "ta": cat})
        return {
            "category": cat,
            "confidence": 0.85,
            "label_en": friendly["en"],
            "label_ta": friendly["ta"],
            "distribution": {cat: 0.85},
            "keywords": extract_keywords(cleaned, top_k=6)
        }

classifier = DocumentClassifier()

def get_classifier():
    return classifier
