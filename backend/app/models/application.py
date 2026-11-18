"""
Application Tracker ORM model.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from ..database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), default="Scholarship")  # Scholarship, Admission, Job, Internship, Scheme
    deadline = Column(String(50), nullable=True)
    status = Column(String(50), default="Draft")  # Draft, In Progress, Ready for Review, Submitted, Under Review, Completed, Rejected
    progress_percent = Column(Integer, default=15)
    portal_url = Column(String(512), nullable=True)
    notes = Column(Text, default="")
    checklist = Column(JSON, default=list)  # list of { "item": str, "done": bool, "required": bool }
    reminder_date = Column(String(50), nullable=True)
    attached_doc_ids = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
