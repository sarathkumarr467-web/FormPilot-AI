"""
Document and Upload ORM model.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean
from ..database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    file_type = Column(String(50), default="pdf")
    doc_category = Column(String(100), default="unclassified")  # from ML classifier
    doc_category_confidence = Column(String(20), default="0.0")
    page_count = Column(Integer, default=1)
    extracted_text = Column(Text, default="")
    is_blank_form = Column(Boolean, default=False)
    is_filled_form = Column(Boolean, default=False)
    is_guideline = Column(Boolean, default=False)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
