"""
AI Application Assistant Chat API for FormPilot AI.
Grounds responses on the active document, provides bilingual Tamil and English answers,
and explains tricky declarations.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.document import Document
from ..models.chat import ChatMessage
from ..schemas.schemas import ChatRequest, ChatResponse
from ..services.ai_assistant import AIAssistantService

router = APIRouter(prefix="/assistant", tags=["Assistant"])

@router.post("/chat", response_model=ChatResponse)
def assistant_chat(req: ChatRequest, user_id: int = 1, db: Session = Depends(get_db)):
    doc_context = ""
    if req.document_id:
        doc = db.query(Document).filter(Document.id == req.document_id).first()
        if doc and doc.extracted_text:
            doc_context = doc.extracted_text

    # Log user message
    user_msg = ChatMessage(
        user_id=user_id,
        document_id=req.document_id,
        role="user",
        content=req.message,
        language=req.language
    )
    db.add(user_msg)

    # Generate assistant reply
    res = AIAssistantService.chat(
        message=req.message,
        doc_context=doc_context,
        language=req.language,
        history=req.conversation_history
    )

    # Log assistant message
    asst_msg = ChatMessage(
        user_id=user_id,
        document_id=req.document_id,
        role="assistant",
        content=res["reply"],
        language=res["language"]
    )
    db.add(asst_msg)
    db.commit()

    return res

@router.get("/history")
def get_chat_history(user_id: int = 1, document_id: int = None, db: Session = Depends(get_db)):
    query = db.query(ChatMessage).filter(ChatMessage.user_id == user_id)
    if document_id:
        query = query.filter(ChatMessage.document_id == document_id)
    msgs = query.order_by(ChatMessage.created_at.asc()).limit(50).all()
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "language": m.language,
            "created_at": m.created_at.strftime("%H:%M")
        }
        for m in msgs
    ]
