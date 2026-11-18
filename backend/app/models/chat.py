"""
AI Assistant conversation messages ORM model.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from ..database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True, index=True)
    role = Column(String(20), default="user")  # user, assistant, system
    content = Column(Text, nullable=False)
    language = Column(String(10), default="en")  # en, ta
    created_at = Column(DateTime, default=datetime.utcnow)
