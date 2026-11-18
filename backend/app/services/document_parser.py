"""
Multi-format Document Parser for FormPilot AI.
Extracts text, metadata, page counts, and structural blocks from:
- PDF (.pdf) via PyMuPDF (fitz) and pdfplumber
- Word Documents (.docx, .doc) via python-docx
- Images (.png, .jpg, .jpeg, .webp, .tiff, .bmp) via OCR and PIL
- Spreadsheets (.xlsx, .xls, .csv) via pandas
- Plain text & Rich text (.txt, .rtf)
"""
import os
import re
from typing import Dict, Any, List
from PIL import Image

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import docx
except ImportError:
    docx = None

try:
    import pandas as pd
except ImportError:
    pd = None

class DocumentParser:
    @staticmethod
    def parse_file(file_path: str, filename: str) -> Dict[str, Any]:
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        
        result = {
            "filename": filename,
            "extension": ext,
            "text": "",
            "pages": 1,
            "sections": [],
            "metadata": {}
        }
        
        if ext == "pdf":
            return DocumentParser._parse_pdf(file_path, result)
        elif ext in ["docx", "doc"]:
            return DocumentParser._parse_docx(file_path, result)
        elif ext in ["png", "jpg", "jpeg", "webp", "tiff", "bmp"]:
            return DocumentParser._parse_image(file_path, result)
        elif ext in ["xlsx", "xls"]:
            return DocumentParser._parse_excel(file_path, result)
        elif ext == "csv":
            return DocumentParser._parse_csv(file_path, result)
        elif ext in ["txt", "rtf"]:
            return DocumentParser._parse_txt(file_path, result)
        else:
            # Fallback raw text attempt
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    result["text"] = f.read()
            except Exception:
                result["text"] = ""
            return result

    @staticmethod
    def _parse_pdf(file_path: str, result: Dict[str, Any]) -> Dict[str, Any]:
        text_content = []
        page_count = 1
        
        # 1. Try PyMuPDF (fitz)
        if fitz:
            try:
                doc = fitz.open(file_path)
                page_count = len(doc)
                result["metadata"]["title"] = doc.metadata.get("title", "")
                result["metadata"]["author"] = doc.metadata.get("author", "")
                
                for i, page in enumerate(doc):
                    t = page.get_text()
                    if t.strip():
                        text_content.append(t)
                doc.close()
            except Exception as e:
                print(f"[DocumentParser] fitz error: {e}")
                
        # 2. Try pdfplumber if fitz extracted little or empty text
        if (not text_content or len(" ".join(text_content).strip()) < 50) and pdfplumber:
            try:
                with pdfplumber.open(file_path) as pdf:
                    page_count = len(pdf.pages)
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text_content.append(extracted)
            except Exception as e:
                print(f"[DocumentParser] pdfplumber error: {e}")
                
        full_text = "\n\n".join(text_content)
        result["text"] = full_text.strip()
        result["pages"] = page_count
        return result

    @staticmethod
    def _parse_docx(file_path: str, result: Dict[str, Any]) -> Dict[str, Any]:
        if not docx:
            result["text"] = "DOCX parser module not available"
            return result
        try:
            doc = docx.Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            
            # Also extract text from tables
            table_text = []
            for table in doc.tables:
                for row in table.rows:
                    row_data = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_data:
                        table_text.append(" | ".join(row_data))
                        
            all_text = paragraphs + table_text
            result["text"] = "\n".join(all_text)
            result["pages"] = max(1, len(all_text) // 25)
        except Exception as e:
            result["text"] = f"Error reading Word document: {str(e)}"
        return result

    @staticmethod
    def _parse_image(file_path: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Process image file with OCR fallback."""
        try:
            with Image.open(file_path) as img:
                result["metadata"]["width"] = img.width
                result["metadata"]["height"] = img.height
                result["metadata"]["format"] = img.format
                
            # Attempt pytesseract if available on system
            try:
                import pytesseract
                extracted = pytesseract.image_to_string(Image.open(file_path))
                if extracted.strip():
                    result["text"] = extracted.strip()
                    return result
            except Exception:
                pass
                
            # Fallback intelligent visual descriptor
            result["text"] = f"Scanned Document Image: {os.path.basename(file_path)} [{img.width}x{img.height}]"
        except Exception as e:
            result["text"] = f"Error opening image: {str(e)}"
        return result

    @staticmethod
    def _parse_excel(file_path: str, result: Dict[str, Any]) -> Dict[str, Any]:
        if pd:
            try:
                df = pd.read_excel(file_path)
                result["text"] = df.to_string()
                result["pages"] = 1
            except Exception as e:
                result["text"] = f"Error reading Excel file: {str(e)}"
        return result

    @staticmethod
    def _parse_csv(file_path: str, result: Dict[str, Any]) -> Dict[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                result["text"] = f.read()
        except Exception as e:
            result["text"] = f"Error reading CSV: {str(e)}"
        return result

    @staticmethod
    def _parse_txt(file_path: str, result: Dict[str, Any]) -> Dict[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                result["text"] = f.read()
        except Exception as e:
            result["text"] = f"Error reading text file: {str(e)}"
        return result
