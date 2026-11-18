"""
Rules-based Eligibility Guidance Engine for FormPilot AI.
Evaluates applicant profile criteria against official scholarship, college admission,
and government scheme rules with transparent rule justifications in English and Tamil.
"""
from typing import Dict, Any, List

SCHEME_DATABASE = {
    "post_matric_scholarship": {
        "id": "post_matric_scholarship",
        "name_en": "Post-Matric Scholarship for SC/ST/OBC Students",
        "name_ta": "எஸ்சி/எஸ்டி/ஓபிசி மாணவர்களுக்கான போஸ்ட்-மெட்ரிக் கல்வி உதவித்தொகை",
        "category": "Scholarship",
        "official_portal": "https://scholarships.gov.in",
        "rules": [
            {
                "id": "income_limit",
                "desc_en": "Annual family income must not exceed ₹2,50,000 for eligible categories.",
                "desc_ta": "குடும்ப ஆண்டு வருமானம் ₹2,50,000க்கு மிகாமல் இருக்க வேண்டும்.",
                "check": lambda p: p.get("annual_family_income", 0) <= 250000
            },
            {
                "id": "education_level",
                "desc_en": "Must be enrolled in post-matriculation courses (Class 11, 12, ITI, Diploma, Degree, PG).",
                "desc_ta": "பத்தாம் வகுப்புக்கு மேற்பட்ட படிப்புகளில் பயில வேண்டும் (11, 12, டிப்ளமோ, பட்டப்படிப்பு).",
                "check": lambda p: p.get("education_level") in ["Higher Secondary", "Diploma", "Undergraduate", "Postgraduate", "PhD"]
            },
            {
                "id": "category",
                "desc_en": "Applicant must belong to SC, ST, OBC, or DNT categories.",
                "desc_ta": "விண்ணப்பதாரர் SC, ST, OBC அல்லது DNT பிரிவைச் சேர்ந்தவராக இருக்க வேண்டும்.",
                "check": lambda p: p.get("category_caste") in ["SC", "ST", "OBC", "MBC", "BC"]
            }
        ]
    },
    "aicte_pragati": {
        "id": "aicte_pragati",
        "name_en": "AICTE Pragati Scholarship for Girl Students",
        "name_ta": "மாணவிகளுக்கான ஏஐசிடிஇ பிரகதி கல்வி உதவித்தொகை",
        "category": "Scholarship",
        "official_portal": "https://www.aicte-india.org/schemes/students-development-schemes/Pragati",
        "rules": [
            {
                "id": "gender",
                "desc_en": "Scheme is exclusively for female students.",
                "desc_ta": "இத்திட்டம் மாணவிகளுக்கு மட்டுமே பொருந்தும்.",
                "check": lambda p: str(p.get("gender", "")).lower() in ["female", "girl", "woman"]
            },
            {
                "id": "income_limit",
                "desc_en": "Family income must be less than ₹8,00,000 per annum.",
                "desc_ta": "குடும்ப ஆண்டு வருமானம் ₹8,00,000க்கு குறைவாக இருக்க வேண்டும்.",
                "check": lambda p: p.get("annual_family_income", 0) <= 800000
            },
            {
                "id": "course",
                "desc_en": "Must be admitted in 1st year of Degree/Diploma in an AICTE approved technical institution.",
                "desc_ta": "AICTE அங்கீகரிக்கப்பட்ட கல்வி நிறுவனத்தில் முதல் ஆண்டு பட்டப்படிப்பு/டிப்ளமோவில் சேர்ந்திருக்க வேண்டும்.",
                "check": lambda p: p.get("education_level") in ["Undergraduate", "Diploma"]
            }
        ]
    },
    "central_sector_scholarship": {
        "id": "central_sector_scholarship",
        "name_en": "Central Sector Scheme of Scholarships for College & University Students",
        "name_ta": "கல்லூரி மாணவர்களுக்கான மத்திய துறை கல்வி உதவித்தொகை திட்டம்",
        "category": "Scholarship",
        "official_portal": "https://scholarships.gov.in",
        "rules": [
            {
                "id": "marks_cutoff",
                "desc_en": "Minimum 80th percentile in relevant stream in Class 12th board exams (approx. >= 80%).",
                "desc_ta": "12 ஆம் வகுப்பு பொதுத் தேர்வில் குறைந்தது 80% மதிப்பெண்கள் பெற்றிருக்க வேண்டும்.",
                "check": lambda p: p.get("marks_percentage", 0) >= 80.0
            },
            {
                "id": "income_limit",
                "desc_en": "Annual family income must not exceed ₹4,50,000.",
                "desc_ta": "குடும்ப ஆண்டு வருமானம் ₹4,50,000க்கு மிகாமல் இருக்க வேண்டும்.",
                "check": lambda p: p.get("annual_family_income", 0) <= 450000
            },
            {
                "id": "course",
                "desc_en": "Must be enrolled in regular undergraduate degree courses.",
                "desc_ta": "முழுநேர இளங்கலை பட்டப்படிப்பில் பயில வேண்டும்.",
                "check": lambda p: p.get("education_level") == "Undergraduate"
            }
        ]
    },
    "tn_pudhumai_penn": {
        "id": "tn_pudhumai_penn",
        "name_en": "Tamil Nadu Pudhumai Penn Higher Education Scheme (₹1,000/month)",
        "name_ta": "தமிழ்நாடு புதுமைப் பெண் உயர்கல்வி உறுதித் திட்டம் (மாதம் ₹1,000)",
        "category": "Government Scheme",
        "official_portal": "https://www.pudhumaipenn.tn.gov.in",
        "rules": [
            {
                "id": "gender",
                "desc_en": "Exclusively for girl students.",
                "desc_ta": "மாணவிகளுக்கு மட்டுமே உரியது.",
                "check": lambda p: str(p.get("gender", "")).lower() in ["female", "girl", "woman"]
            },
            {
                "id": "state",
                "desc_en": "Applicant must reside and study in Tamil Nadu.",
                "desc_ta": "விண்ணப்பதாரர் தமிழ்நாட்டில் வசிப்பவராகவும் படிப்பவராகவும் இருக்க வேண்டும்.",
                "check": lambda p: "tamil nadu" in str(p.get("state", "")).lower()
            },
            {
                "id": "education_level",
                "desc_en": "Must be enrolled in recognized undergraduate degree, diploma, or ITI course.",
                "desc_ta": "அங்கீகரிக்கப்பட்ட பட்டப்படிப்பு அல்லது டிப்ளமோவில் சேர்ந்திருக்க வேண்டும்.",
                "check": lambda p: p.get("education_level") in ["Undergraduate", "Diploma", "Vocational"]
            }
        ]
    }
}

class EligibilityEngine:
    @staticmethod
    def get_supported_schemes() -> List[Dict[str, Any]]:
        return [
            {
                "id": v["id"],
                "name_en": v["name_en"],
                "name_ta": v["name_ta"],
                "category": v["category"],
                "portal": v["official_portal"]
            }
            for v in SCHEME_DATABASE.values()
        ]

    @staticmethod
    def evaluate(profile: Dict[str, Any], scheme_id: str = "post_matric_scholarship") -> Dict[str, Any]:
        scheme = SCHEME_DATABASE.get(scheme_id)
        if not scheme:
            # Default to post_matric_scholarship
            scheme = SCHEME_DATABASE["post_matric_scholarship"]

        rules_evaluated = []
        passed_rules = 0
        failed_reasons_en = []
        failed_reasons_ta = []

        for rule in scheme["rules"]:
            try:
                passed = bool(rule["check"](profile))
            except Exception:
                passed = False
                
            rules_evaluated.append({
                "rule_id": rule["id"],
                "description_en": rule["desc_en"],
                "description_ta": rule["desc_ta"],
                "passed": passed
            })
            
            if passed:
                passed_rules += 1
            else:
                failed_reasons_en.append(rule["desc_en"])
                failed_reasons_ta.append(rule["desc_ta"])

        total_rules = len(scheme["rules"])
        confidence = round(passed_rules / total_rules, 2) if total_rules > 0 else 0.0

        if passed_rules == total_rules:
            status = "eligible"
            label_en = "Appears Eligible"
            label_ta = "விண்ணப்பிக்க தகுதியுடையவர்"
            actions_en = [
                "Proceed to gather mandatory certificates (Income, Community, Bonafide).",
                f"Apply directly on the official portal: {scheme['official_portal']}",
                "Use FormPilot Create & Fill module to prepare your application draft."
            ]
            actions_ta = [
                "தேவையான சான்றிதழ்களை (வருமானம், சாதி, போனஃபைடு) தயார் செய்யவும்.",
                f"அதிகாரப்பூர்வ தளத்தில் விண்ணப்பிக்கவும்: {scheme['official_portal']}",
                "விண்ணப்பத்தை எளிதாக நிரப்ப FormPilot-ஐப் பயன்படுத்தவும்."
            ]
        elif passed_rules >= 1 and (total_rules - passed_rules) == 1:
            status = "more_info_needed"
            label_en = "Requires Verification / Close Match"
            label_ta = "கூடுதல் சரிபார்ப்பு தேவை"
            actions_en = [
                f"You missed the following requirement: {failed_reasons_en[0]}",
                "Verify whether you qualify for relaxation (e.g. category-based income limits).",
                "Consult the institution nodal officer."
            ]
            actions_ta = [
                f"பின்வரும் விதியை பூர்த்தி செய்ய வேண்டும்: {failed_reasons_ta[0]}",
                "விதிவிலக்குகள் ஏதேனும் உள்ளதா என சரிபார்க்கவும்.",
                "கல்லூரி உதவித்தொகை அதிகாரியை அணுகவும்."
            ]
        else:
            status = "not_eligible"
            label_en = "Appears Not Eligible"
            label_ta = "தகுதி பெறவில்லை"
            actions_en = [
                "You do not meet the primary eligibility criteria for this scheme.",
                "Explore alternate schemes matching your profile in FormPilot Application Guide."
            ]
            actions_ta = [
                "இத்திட்டத்திற்கான முக்கிய தகுதி வரம்புகளை நீங்கள் பூர்த்தி செய்யவில்லை.",
                "உங்கள் சுயவிவரத்திற்கு ஏற்ற பிற திட்டங்களை ஆராயுங்கள்."
            ]

        return {
            "scheme_id": scheme["id"],
            "scheme_name_en": scheme["name_en"],
            "scheme_name_ta": scheme["name_ta"],
            "status": status,
            "status_label_en": label_en,
            "status_label_ta": label_ta,
            "confidence": confidence,
            "reasons_en": failed_reasons_en if failed_reasons_en else ["All primary criteria met."],
            "reasons_ta": failed_reasons_ta if failed_reasons_ta else ["அனைத்து முதன்மை விதிகளும் பூர்த்தி செய்யப்பட்டுள்ளன."],
            "rules_evaluated": rules_evaluated,
            "suggested_actions_en": actions_en,
            "suggested_actions_ta": actions_ta,
            "official_portal": scheme["official_portal"]
        }
