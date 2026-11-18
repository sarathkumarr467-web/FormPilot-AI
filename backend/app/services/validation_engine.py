"""
Validation and Error Detection Engine for FormPilot AI.
Performs deterministic and format checks on form fields and cross-document integrity.
"""
import re
from datetime import datetime
from typing import Dict, Any, List

class ValidationEngine:
    @staticmethod
    def validate_field(field_id: str, label: str, value: str, is_mandatory: bool = True) -> Dict[str, Any]:
        """Validate an individual form field value."""
        val = (value or "").strip()
        label_lower = label.lower()
        
        # Check mandatory empty
        if not val:
            if is_mandatory:
                return {
                    "is_valid": False,
                    "error_en": f"Mandatory field '{label}' is missing or empty.",
                    "error_ta": f"கட்டாயப் புலமான '{label}' பூர்த்தி செய்யப்படவில்லை.",
                    "suggested_correction": "Please enter a valid value."
                }
            return {"is_valid": True}
            
        # 1. Email validation
        if "email" in label_lower or "e-mail" in label_lower or "mail id" in label_lower:
            email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if not re.match(email_pattern, val):
                return {
                    "is_valid": False,
                    "error_en": f"Invalid email format: '{val}'. Expected format: name@example.com",
                    "error_ta": f"தவறான மின்னஞ்சல் வடிவம்: '{val}'. வடிவம்: name@example.com",
                    "suggested_correction": "Check for typos like missing '@' or '.com'"
                }
                
        # 2. Phone / Mobile validation (Indian 10-digit standard or with +91)
        if any(k in label_lower for k in ["phone", "mobile", "contact", "cell"]):
            clean_phone = re.sub(r"[\s\-\+]", "", val)
            if clean_phone.startswith("91") and len(clean_phone) == 12:
                clean_phone = clean_phone[2:]
            if not (clean_phone.isdigit() and len(clean_phone) == 10 and clean_phone[0] in "6789"):
                return {
                    "is_valid": False,
                    "error_en": f"Invalid Indian mobile number: '{val}'. Must be 10 digits starting with 6, 7, 8, or 9.",
                    "error_ta": f"தவறான கைபேசி எண்: '{val}'. 10 இலக்கங்கள் 6, 7, 8 அல்லது 9 இல் தொடங்க வேண்டும்.",
                    "suggested_correction": "Enter a valid 10-digit mobile number."
                }

        # 3. PIN Code (Indian 6-digit postal code)
        if any(k in label_lower for k in ["pin", "pincode", "postal code"]):
            clean_pin = re.sub(r"\s+", "", val)
            if not (clean_pin.isdigit() and len(clean_pin) == 6 and clean_pin[0] != "0"):
                return {
                    "is_valid": False,
                    "error_en": f"Invalid PIN code: '{val}'. Indian postal PIN codes must be 6 digits and cannot start with 0.",
                    "error_ta": f"தவறான அஞ்சல் குறியீட்டு எண் (PIN): '{val}'. 6 இலக்கங்கள் இருக்க வேண்டும்.",
                    "suggested_correction": "Provide a 6-digit postal code (e.g., 600001)."
                }

        # 4. Aadhaar Number (12 digits)
        if "aadhaar" in label_lower or "uidai" in label_lower:
            clean_uid = re.sub(r"[\s\-]", "", val)
            if not (clean_uid.isdigit() and len(clean_uid) == 12):
                return {
                    "is_valid": False,
                    "error_en": f"Invalid Aadhaar number format: '{val}'. Must be exactly 12 numeric digits.",
                    "error_ta": f"தவறான ஆதார் எண் வடிவம்: '{val}'. 12 இலக்க எண்களைக் கொண்டிருக்க வேண்டும்.",
                    "suggested_correction": "Enter 12 digits (e.g., 1234 5678 9012)."
                }

        # 5. PAN Number (5 letters + 4 digits + 1 letter, e.g. ABCDE1234F)
        if "pan" in label_lower and ("card" in label_lower or "number" in label_lower):
            clean_pan = val.upper().strip()
            pan_pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
            if not re.match(pan_pattern, clean_pan):
                return {
                    "is_valid": False,
                    "error_en": f"Invalid PAN format: '{val}'. Standard format: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F).",
                    "error_ta": f"தவறான பான் (PAN) அட்டை எண்: '{val}'. வடிவம்: 5 எழுத்துக்கள், 4 எண்கள், 1 எழுத்து.",
                    "suggested_correction": "Check format: ABCDE1234F"
                }

        # 6. Date validation (DOB, issuance date)
        if any(k in label_lower for k in ["dob", "birth", "date of birth", "deadline", "date"]):
            date_formats = ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d.%m.%Y"]
            parsed_date = None
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(val, fmt)
                    break
                except ValueError:
                    pass
            if not parsed_date:
                return {
                    "is_valid": False,
                    "error_en": f"Invalid date format: '{val}'. Expected DD-MM-YYYY or YYYY-MM-DD.",
                    "error_ta": f"தவறான தேதி வடிவம்: '{val}'. எதிர்பார்க்கப்படும் வடிவம் DD-MM-YYYY.",
                    "suggested_correction": "Format as DD-MM-YYYY (e.g., 15-08-2003)"
                }
            if "birth" in label_lower and parsed_date > datetime.now():
                return {
                    "is_valid": False,
                    "error_en": "Date of Birth cannot be in the future.",
                    "error_ta": "பிறந்த தேதி எதிர்கால தேதியாக இருக்க முடியாது.",
                    "suggested_correction": "Enter your actual date of birth."
                }

        # 7. Numeric / Currency / Percentage fields
        if any(k in label_lower for k in ["income", "annual income", "fee", "amount", "salary"]):
            clean_num = re.sub(r"[,₹\sRs\.]", "", val)
            if not clean_num.isdigit():
                return {
                    "is_valid": False,
                    "error_en": f"Invalid income/amount value: '{val}'. Numbers only.",
                    "error_ta": f"தவறான வருமான மதிப்பு: '{val}'. எண்கள் மட்டுமே அனுமதிக்கப்படும்.",
                    "suggested_correction": "Enter numerical amount in INR (e.g., 250000)"
                }

        if any(k in label_lower for k in ["percentage", "percent", "marks", "cgpa"]):
            clean_pct = re.sub(r"[%\s]", "", val)
            try:
                pct_val = float(clean_pct)
                if pct_val < 0 or pct_val > 100:
                    return {
                        "is_valid": False,
                        "error_en": f"Percentage out of range: '{val}'. Must be between 0 and 100.",
                        "error_ta": f"சதவீதம் வரம்பிற்கு அப்பாற்பட்டது: '{val}'. 0 முதல் 100க்குள் இருக்க வேண்டும்.",
                        "suggested_correction": "Enter value between 0 and 100 (e.g., 85.5%)"
                    }
            except ValueError:
                return {
                    "is_valid": False,
                    "error_en": f"Invalid percentage format: '{val}'.",
                    "error_ta": f"தவறான சதவீத வடிவம்: '{val}'.",
                    "suggested_correction": "Enter a number like 82.5%"
                }

        return {"is_valid": True}

    @staticmethod
    def cross_check_mismatch(doc_a_data: Dict[str, str], doc_b_data: Dict[str, str]) -> List[Dict[str, Any]]:
        """Detect cross-document information mismatch (e.g., between Aadhaar and Marksheet)."""
        mismatches = []
        
        # Check Name mismatch
        name_a = (doc_a_data.get("name") or doc_a_data.get("full_name") or "").strip().lower()
        name_b = (doc_b_data.get("name") or doc_b_data.get("full_name") or "").strip().lower()
        if name_a and name_b and name_a != name_b:
            mismatches.append({
                "field": "Name",
                "doc_a_value": doc_a_data.get("name"),
                "doc_b_value": doc_b_data.get("name"),
                "issue_en": f"Name spelling discrepancy detected: '{doc_a_data.get('name')}' vs '{doc_b_data.get('name')}'.",
                "issue_ta": f"பெயர் எழுத்துப்பிழை முரண்பாடு கண்டறியப்பட்டது: '{doc_a_data.get('name')}' vs '{doc_b_data.get('name')}'.",
                "severity": "high",
                "suggestion": "Ensure the name matches your official 10th certificate or Gazette notification."
            })
            
        # Check DOB mismatch
        dob_a = doc_a_data.get("dob") or doc_a_data.get("date_of_birth")
        dob_b = doc_b_data.get("dob") or doc_b_data.get("date_of_birth")
        if dob_a and dob_b and dob_a != dob_b:
            mismatches.append({
                "field": "Date of Birth",
                "doc_a_value": dob_a,
                "doc_b_value": dob_b,
                "issue_en": f"Date of Birth mismatch detected: '{dob_a}' vs '{dob_b}'.",
                "issue_ta": f"பிறந்த தேதி முரண்பாடு கண்டறியப்பட்டது: '{dob_a}' vs '{dob_b}'.",
                "severity": "critical",
                "suggestion": "Double-check your proof of birth document."
            })
            
        return mismatches
