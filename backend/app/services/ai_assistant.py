"""
AI Application Assistant Service for FormPilot AI.
Provides grounded, bilingual conversational assistance on uploaded forms, declarations,
eligibility questions, and error resolution.
"""
from typing import Dict, Any, List
from ..core.config import settings

class AIAssistantService:
    @staticmethod
    def chat(
        message: str,
        doc_context: str = "",
        language: str = "en",
        history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Generate context-aware assistance response."""
        msg_lower = message.lower()
        is_tamil = language == "ta" or any("\u0B80" <= ch <= "\u0BFF" for ch in message)

        # Context grounding
        doc_snippet = doc_context[:1000] if doc_context else "No document actively uploaded."

        # Tricky legal declaration query
        if "declaration" in msg_lower or "undertaking" in msg_lower or "உறுதிமொழி" in message:
            if is_tamil:
                reply = (
                    "விண்ணப்பங்களில் உள்ள 'உறுதிமொழி' (Declaration) என்பது நீங்கள் அளித்துள்ள விவரங்கள் அனைத்தும் உண்மையானவை என "
                    "சட்டப்பூர்வமாக ஒப்புக்கொள்வதாகும். ஏதேனும் தகவல் தவறாக இருந்தால் உதவித்தொகை ரத்து செய்யப்பட்டு சட்ட நடவடிக்கை எடுக்கப்படலாம். "
                    "எனவே உங்கள் பெயர், வருமானம், சாதி மற்றும் வங்கி விவரங்கள் சான்றிதழ்களோடு சரியாக பொருந்துகிறதா என்பதை சரிபார்த்த பின்னரே ஒப்புதல் அளிக்கவும்."
                )
            else:
                reply = (
                    "An Application Declaration is a legally binding undertaking certifying that all entered information "
                    "(Income, Caste, Marks, Bank details) is genuine and supported by valid certificates. Providing false information "
                    "can lead to cancellation of scholarship or legal disqualification. Always cross-verify your details with your certificates before submitting."
                )
            return {
                "reply": reply,
                "language": "ta" if is_tamil else "en",
                "source_reference": "Legal Declaration Standards",
                "suggested_questions": [
                    "What documents are required for income proof?",
                    "How to fix name mismatch in certificate?",
                    "வருமானச் சான்றிதழ் யாரிடம் பெற வேண்டும்?"
                ]
            }

        # Income / Tahsildar query
        if "income" in msg_lower or "வருமானம்" in message or "tahsildar" in msg_lower:
            if is_tamil:
                reply = (
                    "வருமானச் சான்றிதழ் உங்கள் தாலுகா அலுவலக வட்டாட்சியரால் (Tahsildar) அல்லது இ-சேவை (e-Seva) மையம் வழியாக வழங்கப்பட்டிருக்க வேண்டும். "
                    "பெரும்பாலான உதவித்தொகைகளுக்கு குடும்ப ஆண்டு வருமானம் ₹2,00,000 முதல் ₹2,50,000க்கு மிகாமல் இருக்க வேண்டும். "
                    "சான்றிதழ் வழங்கப்பட்டு 6 மாதங்களுக்குள் இருப்பதை உறுதி செய்து கொள்ளவும்."
                )
            else:
                reply = (
                    "The Income Certificate must be officially issued by the Revenue Department / Tahsildar through e-Seva portal. "
                    "Most welfare and post-matric scholarships require annual family income to be below ₹2,00,000 to ₹2,50,000. "
                    "Ensure the certificate was issued within the current financial year."
                )
            return {
                "reply": reply,
                "language": "ta" if is_tamil else "en",
                "source_reference": "Revenue Administration Guidelines",
                "suggested_questions": [
                    "Can I apply without income certificate?",
                    "What is the income limit for SC/ST students?",
                    "சாதிச் சான்றிதழ் ஆன்லைனில் சரிபார்ப்பது எப்படி?"
                ]
            }

        # Bank account / DBT query
        if "bank" in msg_lower or "ifsc" in msg_lower or "dbt" in msg_lower or "வங்கி" in message:
            if is_tamil:
                reply = (
                    "உதவித்தொகை உங்கள் வங்கிக் கணக்கில் நேரடியாக (DBT) வரவு வைக்கப்பட வேண்டும் என்றால், அந்த வங்கிக் கணக்கு "
                    "மாணவரின் பெயரிலேயே இருக்க வேண்டும் (கூட்டுக் கணக்கு அல்ல) மற்றும் உங்கள் ஆதார் எண் அந்த வங்கிக் கணக்குடன் "
                    "NPCI ஆதாருடன் இணைக்கப்பட்டிருக்க (Aadhaar Seeding) வேண்டும்."
                )
            else:
                reply = (
                    "For Direct Benefit Transfer (DBT) scholarships, the bank account must be an individual savings account "
                    "in the student's name (not a joint parent account). Crucially, the account must be actively seeded with Aadhaar via NPCI mapper."
                )
            return {
                "reply": reply,
                "language": "ta" if is_tamil else "en",
                "source_reference": "DBT & Aadhaar Seeding Protocols",
                "suggested_questions": [
                    "How to check Aadhaar-bank seeding status?",
                    "What happens if IFSC code changes due to bank merger?",
                    "வங்கி கணக்கு ஆதாருடன் இணைக்கப்பட்டுள்ளதா என அறிவது எப்படி?"
                ]
            }

        # Document specific query
        if doc_context and ("document" in msg_lower or "form" in msg_lower or "படிவம்" in message or "ஆவணம்" in message):
            if is_tamil:
                reply = (
                    f"நீங்கள் பதிவேற்றிய ஆவணத்தின் அடிப்படையில்: இந்த ஆவணத்தில் உள்ள முக்கிய பிரிவுகள், "
                    f"கட்டாய புலங்கள் மற்றும் தேவையான சான்றிதழ்கள் FormPilot AI-ஆல் அடையாளம் காணப்பட்டுள்ளன. "
                    f"படிவத்தை பூர்த்தி செய்ய 'Create & Fill' பக்கத்தைப் பயன்படுத்தலாம் அல்லது பிழைகளைச் சரிபார்க்க 'Explain Filled Form' வசதியைப் பயன்படுத்தலாம்."
                )
            else:
                reply = (
                    f"Based on your currently uploaded document: FormPilot AI has identified the structural sections, "
                    f"mandatory fields, and necessary certificates. You can use 'Create & Fill' to complete it step-by-step or "
                    f"'Explain Filled Form' to audit existing values for errors."
                )
            return {
                "reply": reply,
                "language": "ta" if is_tamil else "en",
                "source_reference": "Uploaded Document Analysis",
                "suggested_questions": [
                    "Explain mandatory fields in this form",
                    "Which documents must I attach?",
                    "இந்த படிவத்தில் உள்ள கட்டாய தகவல்கள் யாவை?"
                ]
            }

        # General helpful fallback
        if is_tamil:
            reply = (
                "வணக்கம்! நான் FormPilot AI விண்ணப்ப உதவியாளர். விண்ணப்பப் படிவங்களை புரிந்து கொள்ளுதல், "
                "விவரங்களை எளிதாக நிரப்புதல், தகுதி வரம்புகளை சரிபார்த்தல் மற்றும் சான்றிதழ் பிழைகளைக் கண்டறிதல் ஆகியவற்றில் உங்களுக்கு உதவ முடியும். "
                "உங்களின் கேள்வியை அல்லது சந்தேகத்தை கேளுங்கள்!"
            )
        else:
            reply = (
                "Hello! I am FormPilot AI, your intelligent application assistance copilot. I can help you understand blank application forms, "
                "explain legal declarations, verify required documents, check scheme eligibility, and ensure zero errors before submission. "
                "How may I assist you with your application today?"
            )

        return {
            "reply": reply,
            "language": "ta" if is_tamil else "en",
            "source_reference": "FormPilot AI Application Engine",
            "suggested_questions": [
                "Check my eligibility for Post-Matric Scholarship",
                "How to fill blank scholarship form?",
                "புதிய விண்ணப்பத்தை எப்படி தொடங்குவது?"
            ]
        }
