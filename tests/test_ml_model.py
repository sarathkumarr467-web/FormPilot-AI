"""
Tests for FormPilot AI Document Classification ML Model.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from ml.predict import classifier

def test_ml_model_loaded():
    assert classifier.model is not None

def test_scholarship_classification():
    text = "Ministry of Social Justice Post-Matric Scholarship Scheme for SC ST student annual family income bank account details"
    pred = classifier.predict(text)
    assert pred["category"] == "scholarship_form"
    assert pred["confidence"] > 0.5
    assert "label_en" in pred
    assert "label_ta" in pred

def test_college_admission_classification():
    text = "Anna University Undergraduate Engineering Admissions TNEA cutoff marks rank certificate verification"
    pred = classifier.predict(text)
    assert pred["category"] == "college_admission"

def test_job_recruitment_classification():
    text = "Staff Selection Commission SSC Combined Graduate Level Exam online recruitment application post applied"
    pred = classifier.predict(text)
    assert pred["category"] == "job_application"

def test_empty_text_handling():
    pred = classifier.predict("")
    assert pred["category"] == "unknown"
