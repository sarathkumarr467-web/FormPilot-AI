"""
Forms Processing API for FormPilot AI.
Powers Blank Form Understanding, AI Form Filling, Filled Form Explanation,
and dynamic PDF Generation.
"""
import os
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.config import settings
from ..models.document import Document
from ..models.analysis import FormAnalysis
from ..models.user import User
from ..schemas.schemas import FormFillRequest, FormFillResponse
from ..services.form_intelligence import FormIntelligenceService
from ..services.validation_engine import ValidationEngine
from ..services.pdf_generator import PDFGenerator

router = APIRouter(prefix="/forms", tags=["Forms"])

@router.post("/analyze")
def analyze_form(
    document_id: Optional[int] = Query(None),
    raw_text: Optional[str] = None,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """Module 1 & 2: Analyze a blank or general application form."""
    text = ""
    filename = "Sample_Application_Form.pdf"
    category = "scholarship_form"

    if document_id:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found.")
        text = doc.extracted_text
        filename = doc.filename
        category = doc.doc_category
    elif raw_text:
        text = raw_text
    else:
        # Default representative blank scholarship application text
        text = (
            "POST-MATRIC SCHOLARSHIP APPLICATION FORM 2026-2027\n"
            "Full Name of Applicant:\nFather Name:\nDate of Birth:\nGender:\n"
            "Email Address:\nMobile Number:\nAadhaar Number:\n"
            "Annual Family Income:\nCommunity Category:\n"
            "College Name:\nDegree Course Name:\nQualifying Exam Percentage:\n"
            "Bank Account Number:\nBank IFSC Code:\nPermanent Address:\n"
            "Declaration: I hereby declare that all information provided is true and correct."
        )

    analysis_res = FormIntelligenceService.analyze_document(text, filename, category)

    # Save analysis in database
    db_analysis = FormAnalysis(
        document_id=document_id,
        user_id=user_id,
        mode="blank_understanding",
        document_title=analysis_res["document_title"],
        detected_type=analysis_res["detected_type"],
        total_fields=analysis_res["total_fields"],
        mandatory_fields_count=analysis_res["mandatory_count"],
        summary_en=analysis_res["summary_en"],
        summary_ta=analysis_res["summary_ta"],
        sections=analysis_res["sections"],
        fields=analysis_res["fields"],
        declarations=analysis_res["declarations"],
        issues_and_errors=[]
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    analysis_res["analysis_id"] = db_analysis.id
    return analysis_res

@router.post("/explain")
def explain_filled_form(
    document_id: Optional[int] = Query(None),
    raw_text: Optional[str] = None,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """Module 4: Analyze an already-filled form to verify answers and detect inconsistencies."""
    text = ""
    filename = "Filled_Application_Review.pdf"

    if document_id:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found.")
        text = doc.extracted_text
        filename = doc.filename
    elif raw_text:
        text = raw_text
    else:
        text = (
            "TAMIL NADU POST-MATRIC SCHOLARSHIP APPLICATION (FILLED COPY)\n"
            "Applicant Name : ARUN KUMAR S\n"
            "Father Name : SURESH KUMAR R\n"
            "Date of Birth : 15-08-2003\n"
            "Gender : Male\n"
            "Email : arun.student@gmail.com\n"
            "Mobile : 9876543210\n"
            "Aadhaar Number : 4839 2048 1092\n"
            "Annual Family Income : 180000\n"
            "Community : OBC\n"
            "College Name : Government College of Technology, Coimbatore\n"
            "Course Name : B.E. Computer Science and Engineering\n"
            "Percentage : 84.5%\n"
            "Bank Account : 304928174920\n"
            "IFSC Code : SBIN0001234\n"
            "Permanent Address : 12, Bharathi Street, Madurai, TN - 625020\n"
            "Declaration : Agreed"
        )

    explanation_res = FormIntelligenceService.explain_filled_form(text, filename)

    # Save to db
    db_analysis = FormAnalysis(
        document_id=document_id,
        user_id=user_id,
        mode="filled_explanation",
        document_title=explanation_res["document_title"],
        detected_type=explanation_res["detected_type"],
        total_fields=explanation_res["total_fields"],
        mandatory_fields_count=explanation_res["mandatory_count"],
        summary_en=explanation_res["summary_en"],
        summary_ta=explanation_res["summary_ta"],
        sections=explanation_res["sections"],
        fields=explanation_res["fields"],
        declarations=explanation_res["declarations"],
        issues_and_errors=explanation_res["issues_and_errors"]
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    explanation_res["analysis_id"] = db_analysis.id
    return explanation_res

@router.post("/fill", response_model=FormFillResponse)
def fill_form(req: FormFillRequest, db: Session = Depends(get_db)):
    """Module 3: Map user answers, validate fields, and generate completed official PDF."""
    user = db.query(User).filter(User.id == (req.user_id or 1)).first()
    user_info = user.profile_data if user and user.profile_data else {
        "full_name": "Arun Kumar S",
        "email": "arun.student@gmail.com",
        "mobile": "9876543210"
    }

    # Fetch document or create standard template fields
    doc_title = "Official Application Form"
    if req.document_id:
        doc = db.query(Document).filter(Document.id == req.document_id).first()
        if doc:
            doc_title = doc.filename

    answers = req.answers or {}
    # If answers is empty, auto-fill from user profile data
    if not answers and user_info:
        answers = {k: str(v) for k, v in user_info.items()}

    # Validate each field
    validation_errors = []
    formatted_fields = []
    
    # Analyze document fields
    base_analysis = FormIntelligenceService.analyze_document("", doc_title)
    for f in base_analysis["fields"]:
        f_id = f["id"]
        # Match from provided answers or user profile
        ans_val = answers.get(f_id) or answers.get(f_id.replace("_", " ")) or str(user_info.get(f_id, ""))
        f["value"] = ans_val

        # Validate
        check = ValidationEngine.validate_field(f_id, f["label_en"], ans_val, f["is_mandatory"])
        if not check["is_valid"]:
            f["status"] = "error"
            f["validation_error"] = check.get("error_en")
            validation_errors.append({
                "field_id": f_id,
                "label": f["label_en"],
                "error_en": check.get("error_en"),
                "error_ta": check.get("error_ta")
            })
        else:
            f["status"] = "verified"

        formatted_fields.append(f)

    # Generate PDF if requested
    pdf_url = None
    if req.export_pdf:
        pdf_path = PDFGenerator.generate_filled_form_pdf(doc_title, user_info, formatted_fields)
        pdf_filename = os.path.basename(pdf_path)
        pdf_url = f"/api/forms/download/{pdf_filename}"

    return {
        "success": len(validation_errors) == 0,
        "total_fields": len(formatted_fields),
        "filled_fields": sum(1 for f in formatted_fields if f["value"]),
        "validation_errors": validation_errors,
        "pdf_download_url": pdf_url,
        "summary_en": f"Completed {sum(1 for f in formatted_fields if f['value'])} of {len(formatted_fields)} fields. {len(validation_errors)} errors detected.",
        "summary_ta": f"{len(formatted_fields)} புலங்களில் {sum(1 for f in formatted_fields if f['value'])} பூர்த்தி செய்யப்பட்டன. {len(validation_errors)} பிழைகள் கண்டறியப்பட்டன."
    }

@router.get("/guide")
def get_application_guide(
    document_id: Optional[int] = Query(None),
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """Module 5: Application Guide - Extract procedure, requirements, and deadlines."""
    text = ""
    filename = "Scheme_Official_Guidelines.pdf"

    if document_id:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if doc:
            text = doc.extracted_text
            filename = doc.filename

    if not text:
        text = (
            "CENTRAL SCHOLARSHIP NOTIFICATION & APPLICATION GUIDELINE 2026\n"
            "Application Window: 01-10-2026 to 30-11-2026. Last date for verification: 15-12-2026.\n"
            "Official Application Website: https://scholarships.gov.in\n"
            "Eligibility: Students with min 80% marks and family income under Rs 4.5 Lakhs per year.\n"
            "Application Fee: No fee for applying online.\n"
            "Mandatory Certificates: Income certificate, 10th and 12th marksheet, Aadhaar card, Bank passbook."
        )

    return FormIntelligenceService.extract_application_guide(text, filename)

@router.get("/download/{filename}")
def download_pdf(filename: str):
    """Download generated application PDF or report."""
    file_path = os.path.join(settings.GENERATED_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Requested PDF file not found.")
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
