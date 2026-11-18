"""
Document Management and Upload API for FormPilot AI.
Supports PDF, DOCX, Images, Excel, CSV, text parsing, OCR, and ML classification.
"""
import os
import shutil
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.config import settings
from ..models.document import Document
from ..services.document_parser import DocumentParser
try:
    from ml.predict import classifier
except ImportError:
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
    from ml.predict import classifier

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    doc_type: Optional[str] = Form("blank_form"),  # blank_form, filled_form, guideline, supporting_doc
    user_id: int = Form(1),
    db: Session = Depends(get_db)
):
    # 1. Validate Extension
    filename = file.filename or "unknown.pdf"
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format '.{ext}'. Supported: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # 2. Save File Locally
    unique_id = uuid.uuid4().hex[:10]
    safe_name = f"{unique_id}_{filename.replace(' ', '_')}"
    saved_path = os.path.join(settings.UPLOAD_DIR, safe_name)

    try:
        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    file_size = os.path.getsize(saved_path)
    if file_size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        os.remove(saved_path)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB."
        )

    # 3. Parse File Content
    parsed = DocumentParser.parse_file(saved_path, filename)
    extracted_text = parsed.get("text", "")
    page_count = parsed.get("pages", 1)

    # 4. Run ML Classification
    ml_pred = classifier.predict(extracted_text)
    category = ml_pred.get("category", "unclassified")
    confidence = str(ml_pred.get("confidence", 0.0))

    # 5. Save to Database
    doc = Document(
        user_id=user_id,
        filename=filename,
        file_path=saved_path,
        file_size_bytes=file_size,
        file_type=ext,
        doc_category=category,
        doc_category_confidence=confidence,
        page_count=page_count,
        extracted_text=extracted_text,
        is_blank_form=(doc_type == "blank_form"),
        is_filled_form=(doc_type == "filled_form"),
        is_guideline=(doc_type == "guideline"),
        metadata_json={
            "ml_prediction": ml_pred,
            "parsed_metadata": parsed.get("metadata", {})
        }
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "success": True,
        "document_id": doc.id,
        "filename": doc.filename,
        "file_type": doc.file_type,
        "page_count": doc.page_count,
        "file_size_bytes": doc.file_size_bytes,
        "ml_classification": ml_pred,
        "is_blank_form": doc.is_blank_form,
        "is_filled_form": doc.is_filled_form,
        "is_guideline": doc.is_guideline,
        "preview_text_snippet": extracted_text[:300] if extracted_text else "No text extracted (OCR fallback enabled)."
    }

@router.get("/list")
def list_documents(user_id: int = 1, db: Session = Depends(get_db)):
    docs = db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).all()
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "file_type": d.file_type,
            "file_size_bytes": d.file_size_bytes,
            "page_count": d.page_count,
            "doc_category": d.doc_category,
            "doc_category_confidence": d.doc_category_confidence,
            "is_blank_form": d.is_blank_form,
            "is_filled_form": d.is_filled_form,
            "is_guideline": d.is_guideline,
            "created_at": d.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for d in docs
    ]

@router.get("/{document_id}")
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {
        "id": doc.id,
        "filename": doc.filename,
        "file_type": doc.file_type,
        "file_size_bytes": doc.file_size_bytes,
        "page_count": doc.page_count,
        "doc_category": doc.doc_category,
        "doc_category_confidence": doc.doc_category_confidence,
        "extracted_text": doc.extracted_text,
        "metadata": doc.metadata_json,
        "created_at": doc.created_at.strftime("%Y-%m-%d %H:%M")
    }

@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    try:
        if os.path.exists(doc.file_path):
            os.remove(doc.file_path)
    except Exception:
        pass
    db.delete(doc)
    db.commit()
    return {"success": True, "message": "Document deleted successfully."}
