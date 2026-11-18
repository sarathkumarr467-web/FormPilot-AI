"""
Tests for FormPilot AI Eligibility Guidance Engine.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from backend.app.services.eligibility_engine import EligibilityEngine

def test_eligible_post_matric_scholarship():
    profile = {
        "age": 19,
        "education_level": "Undergraduate",
        "course": "B.E. Computer Science",
        "annual_family_income": 180000,
        "category_caste": "OBC",
        "marks_percentage": 82.0,
        "state": "Tamil Nadu",
        "gender": "Male"
    }
    result = EligibilityEngine.evaluate(profile, "post_matric_scholarship")
    assert result["status"] == "eligible"
    assert result["confidence"] == 1.0
    assert "scholarships.gov.in" in result["official_portal"]

def test_ineligible_high_income():
    profile = {
        "age": 20,
        "education_level": "Undergraduate",
        "course": "B.Tech",
        "annual_family_income": 950000, # Exceeds income limit
        "category_caste": "General",
        "marks_percentage": 65.0,
        "state": "Tamil Nadu",
        "gender": "Male"
    }
    result = EligibilityEngine.evaluate(profile, "post_matric_scholarship")
    assert result["status"] in ["not_eligible", "more_info_needed"]
    assert len(result["reasons_en"]) >= 1

def test_aicte_pragati_female_only():
    male_profile = {
        "gender": "Male",
        "education_level": "Undergraduate",
        "annual_family_income": 300000
    }
    res_male = EligibilityEngine.evaluate(male_profile, "aicte_pragati")
    assert res_male["status"] != "eligible"

    female_profile = {
        "gender": "Female",
        "education_level": "Undergraduate",
        "annual_family_income": 300000
    }
    res_female = EligibilityEngine.evaluate(female_profile, "aicte_pragati")
    assert res_female["status"] == "eligible"
