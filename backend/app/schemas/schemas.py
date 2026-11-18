"""
Pydantic Schemas for Request & Response validation.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

# Auth Schemas
class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    language_pref: str
    theme_pref: str
    profile_data: Optional[Dict[str, Any]] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    language_pref: Optional[str] = None
    theme_pref: Optional[str] = None
    profile_data: Optional[Dict[str, Any]] = None

# Document Schemas
class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_size_bytes: int
    file_type: str
    doc_category: str
    doc_category_confidence: str
    page_count: int
    created_at: str
    is_blank_form: bool
    is_filled_form: bool
    is_guideline: bool

# Form Processing Schemas
class FieldAnalysis(BaseModel):
    id: str
    label_en: str
    label_ta: str
    section: str
    value: Optional[str] = ""
    explanation_en: str
    explanation_ta: str
    expected_format: str
    example: str
    is_mandatory: bool
    status: str = "pending"  # pending, valid, error, warning
    validation_error: Optional[str] = None

class FormFillRequest(BaseModel):
    document_id: Optional[int] = None
    answers: Dict[str, str]  # field_id -> user answer
    user_id: Optional[int] = None
    export_pdf: bool = True

class FormFillResponse(BaseModel):
    success: bool
    total_fields: int
    filled_fields: int
    validation_errors: List[Dict[str, Any]]
    pdf_download_url: Optional[str] = None
    summary_en: str
    summary_ta: str

# Application Tracker Schemas
class ApplicationCreate(BaseModel):
    title: str
    category: str = "Scholarship"
    deadline: Optional[str] = None
    status: str = "Draft"
    progress_percent: int = 15
    portal_url: Optional[str] = None
    notes: Optional[str] = ""
    checklist: Optional[List[Dict[str, Any]]] = None
    reminder_date: Optional[str] = None

class ApplicationUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    deadline: Optional[str] = None
    status: Optional[str] = None
    progress_percent: Optional[int] = None
    portal_url: Optional[str] = None
    notes: Optional[str] = None
    checklist: Optional[List[Dict[str, Any]]] = None
    reminder_date: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    title: str
    category: str
    deadline: Optional[str]
    status: str
    progress_percent: int
    portal_url: Optional[str]
    notes: Optional[str]
    checklist: List[Dict[str, Any]]
    reminder_date: Optional[str]
    created_at: str

# Eligibility Checker Schemas
class EligibilityCheckRequest(BaseModel):
    scheme_id: Optional[str] = "post_matric_scholarship"
    custom_scheme_name: Optional[str] = None
    age: int
    education_level: str
    course: str
    annual_family_income: float
    category_caste: str
    marks_percentage: float
    state: str = "Tamil Nadu"
    gender: str = "All"
    disability_status: bool = False

class EligibilityCheckResponse(BaseModel):
    status: str  # eligible, not_eligible, more_info_needed
    status_label_en: str
    status_label_ta: str
    confidence: float
    reasons_en: List[str]
    reasons_ta: List[str]
    rules_evaluated: List[Dict[str, Any]]
    suggested_actions_en: List[str]
    suggested_actions_ta: List[str]
    official_portal: Optional[str] = None

# AI Assistant Chat Schemas
class ChatRequest(BaseModel):
    message: str
    document_id: Optional[int] = None
    language: str = "en"  # en, ta
    conversation_history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    reply: str
    language: str
    source_reference: Optional[str] = None
    suggested_questions: List[str]
