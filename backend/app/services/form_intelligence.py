"""
Form Intelligence Service for FormPilot AI.
Powers Form Analysis, Blank Form Understanding, AI Form Filling,
Filled Form Explanation, and Application Guide extraction with Tamil and English support.
"""
import re
from typing import Dict, Any, List
from .validation_engine import ValidationEngine

# Pre-defined field knowledge base for common application forms
COMMON_FIELD_DICTIONARY = {
    "name": {
        "label_en": "Full Name of Applicant",
        "label_ta": "விண்ணப்பதாரரின் முழுப் பெயர்",
        "explanation_en": "Enter your full name as recorded in your 10th / Secondary School certificate. Avoid prefixes like Mr./Ms. unless asked.",
        "explanation_ta": "உங்கள் 10 ஆம் வகுப்பு சான்றிதழில் உள்ளவாறு உங்கள் முழு பெயரை உள்ளிடவும்.",
        "expected_format": "Alphabetic characters (e.g. ARUN KUMAR S)",
        "example": "ARUN KUMAR S",
        "is_mandatory": True,
        "section": "Personal Information"
    },
    "father_name": {
        "label_en": "Father / Guardian Name",
        "label_ta": "தந்தை / பாதுகாவலர் பெயர்",
        "explanation_en": "Name of father or legal guardian as per government identity records.",
        "explanation_ta": "அரசு அடையாள ஆவணங்களின்படி தந்தை அல்லது பாதுகாவலரின் பெயர்.",
        "expected_format": "Full Name in Capital Letters",
        "example": "SURESH KUMAR R",
        "is_mandatory": True,
        "section": "Personal Information"
    },
    "dob": {
        "label_en": "Date of Birth",
        "label_ta": "பிறந்த தேதி",
        "explanation_en": "Your official date of birth as verified by birth certificate or school records.",
        "explanation_ta": "பிறப்புச் சான்றிதழ் அல்லது பள்ளி ஆவணங்களின்படி உங்களின் பிறந்த தேதி.",
        "expected_format": "DD-MM-YYYY",
        "example": "15-08-2003",
        "is_mandatory": True,
        "section": "Personal Information"
    },
    "gender": {
        "label_en": "Gender",
        "label_ta": "பாலினம்",
        "explanation_en": "Select your gender identity as recognized in official records.",
        "explanation_ta": "அதிகாரப்பூர்வ ஆவணங்களில் உள்ள உங்கள் பாலினத்தைத் தேர்ந்தெடுக்கவும்.",
        "expected_format": "Male / Female / Transgender",
        "example": "Male",
        "is_mandatory": True,
        "section": "Personal Information"
    },
    "email": {
        "label_en": "Email Address",
        "label_ta": "மின்னஞ்சல் முகவரி",
        "explanation_en": "Active personal email where application confirmation and OTP notifications will be sent.",
        "explanation_ta": "விண்ணப்ப உறுதிப்படுத்தல் மற்றும் அறிவிப்புகள் வரக்கூடிய தங்களின் நேரடி மின்னஞ்சல் முகவரி.",
        "expected_format": "username@domain.com",
        "example": "arun.student@gmail.com",
        "is_mandatory": True,
        "section": "Contact Details"
    },
    "mobile": {
        "label_en": "Mobile / Phone Number",
        "label_ta": "கைபேசி எண்",
        "explanation_en": "10-digit primary mobile number linked to Aadhaar or bank account for SMS alerts.",
        "explanation_ta": "எஸ்எம்எஸ் அறிவிப்புகளுக்கான 10 இலக்க முதன்மை கைபேசி எண்.",
        "expected_format": "10-digit mobile number",
        "example": "9876543210",
        "is_mandatory": True,
        "section": "Contact Details"
    },
    "aadhaar": {
        "label_en": "Aadhaar Card Number",
        "label_ta": "ஆதார் அட்டை எண்",
        "explanation_en": "12-digit unique identification number issued by UIDAI. Ensure bank account is seeded with this number.",
        "explanation_ta": "UIDAI வழங்கிய 12 இலக்க தனித்துவ அடையாள எண்.",
        "expected_format": "12 numeric digits (XXXX XXXX XXXX)",
        "example": "4839 2048 1092",
        "is_mandatory": True,
        "section": "Identity & Government Records"
    },
    "income": {
        "label_en": "Annual Family Income",
        "label_ta": "குடும்ப ஆண்டு வருமானம்",
        "explanation_en": "Total combined annual income of all family members from all sources (agriculture, salary, business) as stated in the Tahsildar revenue certificate.",
        "explanation_ta": "வட்டாட்சியர் வருமானச் சான்றிதழில் குறிப்பிடப்பட்டுள்ள குடும்பத்தின் மொத்த ஆண்டு வருமானம்.",
        "expected_format": "Amount in INR (without decimals)",
        "example": "₹1,80,000",
        "is_mandatory": True,
        "section": "Socio-Economic Details"
    },
    "community": {
        "label_en": "Community / Caste Category",
        "label_ta": "சமூகப் பிரிவு / சாதி",
        "explanation_en": "Reservation category (General/OC, BC, MBC, SC, ST, EWS) supported by an official community certificate.",
        "explanation_ta": "அரசு சாதிச் சான்றிதழால் உறுதிப்படுத்தப்பட்ட சமூக இடஒதுக்கீட்டுப் பிரிவு.",
        "expected_format": "SC / ST / OBC / MBC / BC / General",
        "example": "OBC",
        "is_mandatory": True,
        "section": "Socio-Economic Details"
    },
    "college_name": {
        "label_en": "Institution / College Name",
        "label_ta": "கல்லூரி / கல்வி நிறுவனத்தின் பெயர்",
        "explanation_en": "Full recognized name of the college or university where you are currently admitted.",
        "explanation_ta": "நீங்கள் தற்போது பயிலும் கல்லூரி அல்லது கல்வி நிறுவனத்தின் முழுப் பெயர்.",
        "expected_format": "College Name & Affiliation",
        "example": "Government College of Technology, Coimbatore",
        "is_mandatory": True,
        "section": "Academic Details"
    },
    "course_name": {
        "label_en": "Degree / Course Name",
        "label_ta": "படிப்பு / பாடப்பிரிவு பெயர்",
        "explanation_en": "Program of study currently enrolled in (e.g. B.E. Computer Science, B.Sc. Maths).",
        "explanation_ta": "தற்போது பயிலும் பட்டப்படிப்பு அல்லது பட்டயப்படிப்பு.",
        "expected_format": "Degree & Specialization",
        "example": "B.E. Computer Science and Engineering",
        "is_mandatory": True,
        "section": "Academic Details"
    },
    "marks_percentage": {
        "label_en": "Previous Qualifying Exam Percentage / CGPA",
        "label_ta": "முந்தைய தேர்வு மதிப்பெண் சதவீதம் / சிஜிபிஏ",
        "explanation_en": "Percentage of marks scored in qualifying examination (e.g. 12th standard or previous semester).",
        "explanation_ta": "முந்தைய தகுதித் தேர்வில் பெற்ற மதிப்பெண் சதவீதம்.",
        "expected_format": "Numeric percentage (0.0 - 100.0%)",
        "example": "84.5%",
        "is_mandatory": True,
        "section": "Academic Details"
    },
    "bank_account": {
        "label_en": "Bank Account Number",
        "label_ta": "வங்கி கணக்கு எண்",
        "explanation_en": "Savings bank account number in the applicant's name for direct benefit transfer (DBT).",
        "explanation_ta": "நேரடி உதவித்தொகை வரவு வைக்கப்பட வேண்டிய மாணவரின் வங்கிக் கணக்கு எண்.",
        "expected_format": "9 to 18 digits",
        "example": "304928174920",
        "is_mandatory": True,
        "section": "Banking & DBT Details"
    },
    "ifsc_code": {
        "label_en": "Bank IFSC Code",
        "label_ta": "வங்கி ஐஎஃப்எஸ்சி (IFSC) குறியீடு",
        "explanation_en": "11-character Indian Financial System Code printed on the bank passbook or cheque book.",
        "explanation_ta": "வங்கி பாஸ்புக்கில் உள்ள 11 எழுத்துக்கள் கொண்ட IFSC குறியீடு.",
        "expected_format": "4 letters + 0 + 6 alphanumeric characters",
        "example": "SBIN0001234",
        "is_mandatory": True,
        "section": "Banking & DBT Details"
    },
    "address": {
        "label_en": "Permanent Residential Address",
        "label_ta": "நிரந்தர குடியிருப்பு முகவரி",
        "explanation_en": "Full door number, street, village/town, district and state as per nativity or residence certificate.",
        "explanation_ta": "இருப்பிடச் சான்றிதழின்படி உங்கள் நிரந்தர வீட்டு முகவரி.",
        "expected_format": "Door No, Street, City, State, PIN",
        "example": "12, Bharathi Street, Gandhi Nagar, Madurai, TN - 625020",
        "is_mandatory": True,
        "section": "Contact Details"
    },
    "declaration_agreed": {
        "label_en": "Truthful Undertaking Declaration",
        "label_ta": "உண்மை அறிவிப்பு உறுதிமொழி",
        "explanation_en": "Legal declaration certifying that all statements are accurate and that disciplinary action can be taken if false.",
        "explanation_ta": "அளிக்கப்பட்ட தகவல்கள் அனைத்தும் உண்மையானவை என்ற சட்டப்பூர்வ உறுதிமொழி.",
        "expected_format": "Yes / Agreed",
        "example": "Agreed",
        "is_mandatory": True,
        "section": "Declarations"
    }
}

class FormIntelligenceService:
    @staticmethod
    def analyze_document(text: str, filename: str, doc_category: str = "scholarship_form") -> Dict[str, Any]:
        """Perform comprehensive structure, field, and requirement analysis on a document."""
        lower_text = text.lower()
        
        # Determine likely document title
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        doc_title = lines[0] if lines else filename
        if len(doc_title) > 80:
            doc_title = doc_title[:80] + "..."
            
        # Detect Sections
        detected_sections = []
        if any(w in lower_text for w in ["personal", "applicant name", "father", "dob", "birth", "gender"]):
            detected_sections.append("Personal Information")
        if any(w in lower_text for w in ["contact", "address", "phone", "mobile", "email", "pin"]):
            detected_sections.append("Contact & Residence Details")
        if any(w in lower_text for w in ["academic", "education", "college", "university", "marks", "percentage", "cgpa"]):
            detected_sections.append("Academic & Course Details")
        if any(w in lower_text for w in ["income", "community", "caste", "tahsildar", "reservation"]):
            detected_sections.append("Socio-Economic & Category Details")
        if any(w in lower_text for w in ["bank", "account", "ifsc", "branch", "dbt"]):
            detected_sections.append("Banking & DBT Details")
        if any(w in lower_text for w in ["declaration", "undertaking", "signature", "hereby declare"]):
            detected_sections.append("Declarations & Verification")
            
        if not detected_sections:
            detected_sections = ["General Information", "Requirements"]

        # Detect Fields from text
        extracted_fields = []
        for key, field_info in COMMON_FIELD_DICTIONARY.items():
            # Check presence of keywords
            is_present = False
            search_terms = [key.replace("_", " ")]
            if key == "name": search_terms.extend(["applicant name", "candidate name", "student name"])
            elif key == "dob": search_terms.extend(["date of birth", "birth date"])
            elif key == "income": search_terms.extend(["annual income", "family income"])
            elif key == "community": search_terms.extend(["caste", "category"])
            elif key == "college_name": search_terms.extend(["institution", "university", "school"])
            elif key == "marks_percentage": search_terms.extend(["percentage", "marks obtained", "cgpa"])
            elif key == "bank_account": search_terms.extend(["account number", "savings bank"])
            
            for term in search_terms:
                if term in lower_text:
                    is_present = True
                    break
                    
            if is_present or doc_category in ["scholarship_form", "college_admission", "job_application"]:
                # Attempt to extract filled value if any (e.g. "Name : John Doe")
                extracted_val = ""
                pattern = rf"(?:{key.replace('_', ' ')})\s*[:\-=]\s*([^\n\r\|]{{2,40}})"
                match = re.search(pattern, lower_text)
                if match:
                    extracted_val = match.group(1).strip()
                    
                field_obj = {
                    "id": key,
                    "label_en": field_info["label_en"],
                    "label_ta": field_info["label_ta"],
                    "section": field_info["section"],
                    "explanation_en": field_info["explanation_en"],
                    "explanation_ta": field_info["explanation_ta"],
                    "expected_format": field_info["expected_format"],
                    "example": field_info["example"],
                    "is_mandatory": field_info["is_mandatory"],
                    "value": extracted_val,
                    "status": "valid" if extracted_val else "pending",
                    "validation_error": None
                }
                
                if extracted_val:
                    val_res = ValidationEngine.validate_field(key, field_info["label_en"], extracted_val, field_info["is_mandatory"])
                    if not val_res["is_valid"]:
                        field_obj["status"] = "error"
                        field_obj["validation_error"] = val_res.get("error_en")
                        
                extracted_fields.append(field_obj)

        # Declarations detected
        declarations = []
        if "declare" in lower_text or "undertaking" in lower_text:
            declarations.append({
                "id": "decl_truth",
                "text_en": "I hereby declare that all statements made in this application are true, complete and correct.",
                "text_ta": "இந்த விண்ணப்பத்தில் கொடுக்கப்பட்டுள்ள அனைத்து தகவல்களும் உண்மையானவை மற்றும் சரியானவை என உறுதியளிக்கிறேன்.",
                "status": "pending_user_consent",
                "importance": "Mandatory Legal Undertaking"
            })
            declarations.append({
                "id": "decl_aadhaar_consent",
                "text_en": "I give my consent to use Aadhaar number for authentication and Direct Benefit Transfer (DBT).",
                "text_ta": "நேரடி உதவித்தொகை (DBT) மற்றும் சரிபார்ப்பிற்கு எனது ஆதார் எண்ணைப் பயன்படுத்த ஒப்புதல் அளிக்கிறேன்.",
                "status": "pending_user_consent",
                "importance": "Required for DBT"
            })

        # Required Documents Checklist
        required_docs = [
            {"name_en": "Class 10 / SSLC Marksheet", "name_ta": "10 ஆம் வகுப்பு மதிப்பெண் பட்டியல்", "mandatory": True},
            {"name_en": "Recent Income Certificate from Tahsildar", "name_ta": "வட்டாட்சியர் வழங்கிய வருமானச் சான்றிதழ்", "mandatory": True},
            {"name_en": "Community / Caste Certificate", "name_ta": "சாதிச் சான்றிதழ்", "mandatory": True},
            {"name_en": "Bonafide Certificate from College", "name_ta": "கல்லூரி பயில்வுச் சான்றிதழ் (Bonafide)", "mandatory": True},
            {"name_en": "Bank Passbook First Page Copy", "name_ta": "வங்கி பாஸ்புக் முதல் பக்க நகல்", "mandatory": True},
            {"name_en": "Aadhaar Card Copy", "name_ta": "ஆதார் அட்டை நகல்", "mandatory": True}
        ]

        summary_en = (
            f"Successfully analyzed '{doc_title}'. Identified {len(detected_sections)} structural sections "
            f"and {len(extracted_fields)} fields ({sum(1 for f in extracted_fields if f['is_mandatory'])} mandatory). "
            f"Bilingual guidance and format rules generated."
        )
        summary_ta = (
            f"'{doc_title}' ஆவணம் வெற்றிகரமாக ஆய்வு செய்யப்பட்டது. {len(detected_sections)} பிரிவுகள் மற்றும் "
            f"{len(extracted_fields)} புலங்கள் கண்டறியப்பட்டன. தமிழ் மற்றும் ஆங்கில வழிகாட்டுதல்கள் தயார்."
        )

        return {
            "document_title": doc_title,
            "detected_type": doc_category.replace("_", " ").title(),
            "sections": detected_sections,
            "fields": extracted_fields,
            "total_fields": len(extracted_fields),
            "mandatory_count": sum(1 for f in extracted_fields if f["is_mandatory"]),
            "declarations": declarations,
            "required_documents": required_docs,
            "summary_en": summary_en,
            "summary_ta": summary_ta
        }

    @staticmethod
    def explain_filled_form(text: str, filename: str) -> Dict[str, Any]:
        """Module 4: Analyze an already-filled form to verify answers and detect inconsistencies."""
        analysis = FormIntelligenceService.analyze_document(text, filename)
        fields = analysis["fields"]
        
        issues = []
        for f in fields:
            val = f.get("value") or ""
            if f["is_mandatory"] and not val:
                issues.append({
                    "field": f["label_en"],
                    "severity": "high",
                    "error_en": f"Mandatory field '{f['label_en']}' is empty or unreadable.",
                    "error_ta": f"கட்டாயப் புலமான '{f['label_ta']}' பூர்த்தி செய்யப்படவில்லை.",
                    "suggested_correction": f"Enter a valid value matching: {f['expected_format']}"
                })
            elif val:
                check = ValidationEngine.validate_field(f["id"], f["label_en"], val, f["is_mandatory"])
                if not check["is_valid"]:
                    issues.append({
                        "field": f["label_en"],
                        "severity": "medium",
                        "error_en": check.get("error_en"),
                        "error_ta": check.get("error_ta"),
                        "suggested_correction": check.get("suggested_correction")
                    })

        analysis["issues_and_errors"] = issues
        analysis["audit_status"] = "PASSED" if len(issues) == 0 else "NEEDS_REVIEW"
        return analysis

    @staticmethod
    def extract_application_guide(text: str, filename: str) -> Dict[str, Any]:
        """Module 5: Extract application procedure, eligibility criteria, dates, and official URLs."""
        # Find dates, deadlines, websites
        dates_found = re.findall(r"\b(?:\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}|\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b", text, re.IGNORECASE)
        urls_found = re.findall(r"https?://[^\s<>\"']+", text)
        
        steps = [
            {
                "step_num": 1,
                "title_en": "Verify Eligibility & Documents",
                "title_ta": "தகுதி மற்றும் ஆவணங்களை சரிபார்க்கவும்",
                "desc_en": "Confirm age, income limits, and gather caste, income, bonafide certificates before applying.",
                "desc_ta": "வயது, வருமான வரம்புகளை சரிபார்த்து சாதி மற்றும் வருமான சான்றிதழ்களை தயார் செய்யவும்."
            },
            {
                "step_num": 2,
                "title_en": "Register on the Official Portal",
                "title_ta": "அதிகாரப்பூர்வ தளத்தில் பதிவு செய்யவும்",
                "desc_en": f"Create your student applicant login on {urls_found[0] if urls_found else 'the designated state/central portal'}.",
                "desc_ta": "அதிகாரப்பூர்வ இணையதளத்தில் உங்கள் மாணவர் கணக்கை பதிவு செய்யவும்."
            },
            {
                "step_num": 3,
                "title_en": "Fill Details & Upload Scanned Documents",
                "title_ta": "விவரங்களை பூர்த்தி செய்து ஆவணங்களை பதிவேற்றவும்",
                "desc_en": "Complete academic, personal, and bank account DBT info. Upload attested copies in PDF/JPEG format.",
                "desc_ta": "கல்வி, வங்கி விவரங்களை பூர்த்தி செய்து சான்றிதழ் நகல்களை பதிவேற்றவும்."
            },
            {
                "step_num": 4,
                "title_en": "Review & Institutional Verification",
                "title_ta": "விண்ணப்ப மதிப்பாய்வு & கல்லூரி ஒப்புதல்",
                "desc_en": "Download the generated PDF acknowledgement and submit one signed copy to your college nodal officer.",
                "desc_ta": "விண்ணப்ப நகலை பதிவிறக்கம் செய்து கையொப்பமிட்டு கல்லூரி அதிகாரியிடம் சமர்ப்பிக்கவும்."
            }
        ]

        return {
            "guide_title": f"Step-by-Step Application Guide: {filename}",
            "important_dates": list(set(dates_found[:4])) if dates_found else ["Refer Official Notification Timeline"],
            "official_websites": list(set(urls_found[:3])) if urls_found else ["https://scholarships.gov.in"],
            "application_fee": "Free of cost / No application fee for standard welfare schemes" if "free" in text.lower() or "no fee" in text.lower() else "Refer official brochure",
            "procedure_steps": steps,
            "source_document": filename
        }
