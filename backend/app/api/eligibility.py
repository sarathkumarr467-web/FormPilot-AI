"""
Eligibility Checker API for FormPilot AI.
Evaluates applicant profile data against official scholarship and scheme rules.
"""
from fastapi import APIRouter
from ..schemas.schemas import EligibilityCheckRequest, EligibilityCheckResponse
from ..services.eligibility_engine import EligibilityEngine

router = APIRouter(prefix="/eligibility", tags=["Eligibility"])

@router.get("/schemes")
def get_supported_schemes():
    return EligibilityEngine.get_supported_schemes()

@router.post("/check", response_model=EligibilityCheckResponse)
def check_eligibility(req: EligibilityCheckRequest):
    profile = {
        "age": req.age,
        "education_level": req.education_level,
        "course": req.course,
        "annual_family_income": req.annual_family_income,
        "category_caste": req.category_caste,
        "marks_percentage": req.marks_percentage,
        "state": req.state,
        "gender": req.gender,
        "disability_status": req.disability_status
    }
    scheme_id = req.scheme_id or "post_matric_scholarship"
    result = EligibilityEngine.evaluate(profile, scheme_id)
    return result
