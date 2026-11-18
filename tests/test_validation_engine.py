"""
Tests for FormPilot AI Validation and Error Detection Engine.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from backend.app.services.validation_engine import ValidationEngine

def test_email_validation():
    # Valid email
    res = ValidationEngine.validate_field("email", "Email Address", "student@example.com")
    assert res["is_valid"] is True

    # Invalid email
    res2 = ValidationEngine.validate_field("email", "Email Address", "invalid-email-at-domain")
    assert res2["is_valid"] is False
    assert "Invalid email format" in res2["error_en"]

def test_mobile_validation():
    # Valid 10-digit Indian mobile
    res = ValidationEngine.validate_field("mobile", "Mobile Number", "9876543210")
    assert res["is_valid"] is True

    # Valid with +91
    res2 = ValidationEngine.validate_field("mobile", "Mobile Number", "+91 9876543210")
    assert res2["is_valid"] is True

    # Invalid (less than 10 digits or invalid starting digit)
    res3 = ValidationEngine.validate_field("mobile", "Mobile Number", "1234567")
    assert res3["is_valid"] is False

def test_pin_code_validation():
    # Valid Indian 6-digit PIN code
    res = ValidationEngine.validate_field("pin", "Postal PIN Code", "600001")
    assert res["is_valid"] is True

    # Invalid (starts with 0 or non-6 digit)
    res2 = ValidationEngine.validate_field("pin", "Postal PIN Code", "012345")
    assert res2["is_valid"] is False

def test_aadhaar_validation():
    # Valid 12 digits
    res = ValidationEngine.validate_field("aadhaar", "Aadhaar Card Number", "4839 2048 1092")
    assert res["is_valid"] is True

    # Invalid (less digits)
    res2 = ValidationEngine.validate_field("aadhaar", "Aadhaar Card Number", "1234")
    assert res2["is_valid"] is False

def test_cross_check_mismatch():
    doc1 = {"name": "Arun Kumar S", "dob": "15-08-2003"}
    doc2 = {"name": "Arun K", "dob": "15-08-2003"}
    mismatches = ValidationEngine.cross_check_mismatch(doc1, doc2)
    assert len(mismatches) == 1
    assert mismatches[0]["field"] == "Name"
