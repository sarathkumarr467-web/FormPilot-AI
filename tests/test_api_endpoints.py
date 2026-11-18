"""
Fast API Endpoint unit tests for FormPilot AI.
Directly tests route controllers with database sessions for fast, reliable execution.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from backend.app.database import SessionLocal, init_db
from backend.app.api.dashboard import get_dashboard_summary
from backend.app.api.eligibility import check_eligibility
from backend.app.api.forms import analyze_form, get_application_guide
from backend.app.api.applications import get_applications
from backend.app.api.ml import get_model_metrics
from backend.app.schemas.schemas import EligibilityCheckRequest

@pytest.fixture(scope="module")
def db_session():
    init_db()
    db = SessionLocal()
    yield db
    db.close()

def test_ml_metrics():
    metrics = get_model_metrics()
    assert "accuracy" in metrics
    assert metrics["accuracy"] >= 0.70

def test_dashboard_summary(db_session):
    data = get_dashboard_summary(user_id=1, db=db_session)
    assert "metrics" in data
    assert data["metrics"]["total_documents"] >= 0
    assert "status_distribution" in data

def test_eligibility_controller():
    req = EligibilityCheckRequest(
        scheme_id="post_matric_scholarship",
        age=20,
        education_level="Undergraduate",
        course="B.E. Computer Science",
        annual_family_income=180000,
        category_caste="OBC",
        marks_percentage=84.5,
        state="Tamil Nadu",
        gender="Male",
        disability_status=False
    )
    result = check_eligibility(req)
    assert result["status"] == "eligible"
    assert result["confidence"] == 1.0

def test_form_analyzer_controller(db_session):
    result = analyze_form(document_id=None, raw_text=None, user_id=1, db=db_session)
    assert "document_title" in result
    assert result["total_fields"] > 0
    assert "summary_en" in result
    assert "summary_ta" in result

def test_application_guide_controller(db_session):
    guide = get_application_guide(document_id=None, user_id=1, db=db_session)
    assert "guide_title" in guide
    assert len(guide["procedure_steps"]) >= 4

def test_applications_controller(db_session):
    apps = get_applications(user_id=1, db=db_session)
    assert len(apps) >= 1
    assert hasattr(apps[0], "__getitem__") or hasattr(apps[0], "title")
