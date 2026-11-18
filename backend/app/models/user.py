"""
User and Profile ORM model.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=True)
    auth_provider = Column(String(50), default="email")  # email, google, supabase
    role = Column(String(50), default="applicant")
    language_pref = Column(String(10), default="en")  # en, ta
    theme_pref = Column(String(10), default="dark")  # dark, light
    profile_data = Column(JSON, default=dict)  # Stores saved profile (DOB, phone, address, education, income, etc.)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
