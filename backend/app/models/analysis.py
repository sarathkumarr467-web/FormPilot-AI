"""
Form Analysis and Intelligence Audit ORM model.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from ..database import Base

class FormAnalysis(Base):
    __tablename__ = "form_analyses"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    mode = Column(String(50), default="analyzer")  # analyzer, blank_understanding, filled_explanation, application_guide
    document_title = Column(String(255), default="Document")
    detected_type = Column(String(100), default="Application Form")
    total_fields = Column(Integer, default=0)
    mandatory_fields_count = Column(Integer, default=0)
    optional_fields_count = Column(Integer, default=0)
    summary_en = Column(Text, default="")
    summary_ta = Column(Text, default="")
    sections = Column(JSON, default=list)
    fields = Column(JSON, default=list)
    declarations = Column(JSON, default=list)
    issues_and_errors = Column(JSON, default=list)
    eligibility_info = Column(JSON, default=dict)
    generated_pdf_path = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
