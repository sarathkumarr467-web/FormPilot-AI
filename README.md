# FormPilot AI — Understand. Fill. Verify. Apply.

> **INNOVATE INDIA Hackathon 2026**  
> **Tagline:** Understand. Fill. Verify. Apply.  
> **Primary Users:** College students, scholarship applicants, job seekers, internship applicants, and government welfare scheme applicants.

---

## 1. Executive Summary & Product Identity

**FormPilot AI** is a production-ready, intelligent AI-powered application assistance web platform. It transforms confusing, high-stakes application processes into simple, transparent, and error-aware digital workflows.

### Core Value Proposition
- **Blank Form Understanding:** Explains every form field, what information to enter, expected data format, realistic examples, and identifies mandatory vs. optional requirements in both **English and Tamil**.
- **AI Form Filling Assistant:** Auto-fills answers from user profile or guided conversational Q&A, validates formats, and dynamically exports a completed official PDF document with legal declarations and signature blocks.
- **Filled Form Explanation:** Scans already-filled applications, validates regex formats (Email, Mobile, PIN, Aadhaar, PAN), detects missing details, checks cross-document spelling or DOB mismatches, and generates an audit report.
- **Application Guide:** Extracts step-by-step procedures, deadlines, eligibility limits, fees, and official links from government notifications and university brochures.
- **Rules-Based Eligibility Checker:** Transparently compares applicant criteria (income ceilings, age limits, reservation categories, marks percentage) against official scheme rules.
- **Document Intelligence Center:** Categorizes supporting identity cards, marksheets, and income certificates, detecting missing or expired documents before submission.
- **Application Tracker:** Full-featured tracker with progress bars, reminders, document checklists, and status transitions (Draft, In Progress, Ready for Review, Submitted, Under Review, Completed, Rejected).
- **Trained Machine Learning Model:** Classifies application document types across 6 distinct categories with verified TF-IDF + Calibrated LinearSVC architecture.

---

## 2. Technology Stack & Architecture

```
+-----------------------------------------------------------------------------------+
|                                 FORMPILOT AI PLATFORM                             |
+-----------------------------------------------------------------------------------+
|  FRONTEND LAYER                                                                   |
|  * Next.js / React 18, TypeScript, Tailwind CSS, Lucide Icons, Chart.js          |
|  * Mandatory Left Sidebar (15 Navigation Items), Collapsible & Mobile Drawer      |
|  * Full Bilingual Engine: English + Natural Tamil (Persisted in localStorage)     |
|  * Theme Engine: Light Mode & Dark Mode (Persisted in localStorage)               |
|  * Project-Relevant AI Hero Visual (1920x1080) at public/images/formpilot-hero.jpg|
+-----------------------------------------------------------------------------------+
|  BACKEND API LAYER (FastAPI)                                                      |
|  * /api/auth          : Registration, Email/Password Login, Google OAuth, Profile |
|  * /api/documents     : Multi-format parsing (PDF, DOCX, TXT, Images, CSV, XLSX) |
|  * /api/forms         : Blank understanding, auto-fill, audit, ReportLab PDF export|
|  * /api/applications  : Application tracker CRUD, checklist, deadlines, progress   |
|  * /api/eligibility   : Rules engine for Post-Matric, Pragati, Central schemes    |
|  * /api/assistant     : Grounded context-aware bilingual chatbot                  |
|  * /api/dashboard     : Real database metrics & distribution statistics           |
|  * /api/ml            : Document classification inference & model evaluation API  |
+-----------------------------------------------------------------------------------+
|  MACHINE LEARNING PIPELINE                                                        |
|  * Text Preprocessing : Unicode NFKC normalization, stopwords, Tamil/English tokens|
|  * Feature Extraction : Sublinear TF-IDF Vectorizer (ngram_range 1-2, 2500 feats) |
|  * Model Architecture : CalibratedClassifierCV + LinearSVC (Stratified 3-Fold CV)  |
|  * Evaluation Metrics : 78.95% Cross-Val Accuracy, 0.7912 Macro F1 Score          |
|  * Artifacts Saved    : ml/models/document_classifier.joblib, metrics.json        |
+-----------------------------------------------------------------------------------+
|  DATABASE & AUTHENTICATION                                                        |
|  * Local Execution    : SQLite (Zero-config development with auto-migration)      |
|  * Production Cloud   : Supabase PostgreSQL with Row Level Security (RLS)         |
+-----------------------------------------------------------------------------------+
```

---

## 3. Left Sidebar Navigation (15 Mandatory Items)

1. **Home** — High-tech hero section with project-relevant background, 3 modes, feature highlights.
2. **Dashboard** — Real metrics (Total Documents, Forms Completed, Pending Apps, Readiness Score).
3. **Form Analyzer** — Upload blank or filled forms, view sections, fields, bilingual guides.
4. **Create & Fill Form** — Guided auto-fill from applicant profile, validation, and PDF download.
5. **Explain Filled Form** — Audit existing applications for format errors and declaration checks.
6. **Application Guide** — Step-by-step procedures, dates, fees, and official portal links.
7. **Document Center** — Manage Aadhaar, marksheets, income certificates, check for missing files.
8. **Eligibility Checker** — Interactive rules engine evaluating user criteria against scheme limits.
9. **Application Tracker** — Track active applications, deadlines, checklists, and status transitions.
10. **History** — Auditing log of completed form analyses.
11. **AI Assistant** — Grounded bilingual conversational assistant.
12. **Profile** — Saved student profile used for 1-click auto-filling.
13. **Settings** — Language toggle (EN / தமிழ்) and Theme toggle (Dark / Light).
14. **Help & Support** — Application FAQ and guidance.
15. **Logout** — Clean session termination.

---

## 4. Machine Learning Model Training & Evaluation

The ML classifier is trained to classify application documents into 6 real-world classes:
- `scholarship_form` (Post-Matric, NSP, Merit-cum-Means, AICTE Pragati)
- `college_admission` (Anna University TNEA, CUET, IIT JEE, Medical, Delhi Univ)
- `job_application` (SSC CGL, UPSC Civil Services, IBPS Bank PO, TCS, Infosys)
- `internship_application` (AICTE Technical Internship, GSoC, Summer Research, ISRO)
- `government_scheme` (PMAY Housing, PM-Kisan, TN Pudhumai Penn, Mudra loan)
- `supporting_document` (Aadhaar, 10th Marksheet, Tahsildar Income Cert, Nativity)

### Reproducible Training Command
```bash
python ml/train.py
```

### Actual Evaluation Results (3-Fold Stratified Cross-Validation)
- **Model Architecture:** Sublinear TF-IDF (1-2 N-grams) + Calibrated LinearSVC
- **Overall Cross-Validation Accuracy:** **78.95%**
- **Macro F1-Score:** **0.7912**

| Class Label | Precision | Recall | F1-Score | Samples |
| :--- | :---: | :---: | :---: | :---: |
| **college_admission** | 0.900 | 1.000 | **0.947** | 9 |
| **government_scheme** | 0.750 | 0.600 | **0.667** | 10 |
| **internship_application** | 0.889 | 0.889 | **0.889** | 9 |
| **job_application** | 0.778 | 0.778 | **0.778** | 9 |
| **scholarship_form** | 0.727 | 0.889 | **0.800** | 9 |
| **supporting_document** | 0.700 | 0.636 | **0.667** | 11 |

*All metrics serialized to `ml/models/metrics.json` and served live via `/api/ml/metrics`.*

---

## 5. Automated Test Results

The comprehensive test suite tests validation regex, rules-based eligibility, trained machine learning inference, and API route controllers:

```bash
python -m pytest tests -p no:anyio -v
```

### Actual Test Execution Output:
```
tests/test_api_endpoints.py::test_ml_metrics PASSED                      [  5%]
tests/test_api_endpoints.py::test_dashboard_summary PASSED               [ 10%]
tests/test_api_endpoints.py::test_eligibility_controller PASSED          [ 15%]
tests/test_api_endpoints.py::test_form_analyzer_controller PASSED        [ 21%]
tests/test_api_endpoints.py::test_application_guide_controller PASSED    [ 26%]
tests/test_api_endpoints.py::test_applications_controller PASSED         [ 31%]
tests/test_eligibility.py::test_eligible_post_matric_scholarship PASSED  [ 36%]
tests/test_eligibility.py::test_ineligible_high_income PASSED            [ 42%]
tests/test_eligibility.py::test_aicte_pragati_female_only PASSED         [ 47%]
tests/test_ml_model.py::test_ml_model_loaded PASSED                      [ 52%]
tests/test_ml_model.py::test_scholarship_classification PASSED           [ 57%]
tests/test_ml_model.py::test_college_admission_classification PASSED     [ 63%]
tests/test_ml_model.py::test_job_recruitment_classification PASSED       [ 68%]
tests/test_ml_model.py::test_empty_text_handling PASSED                  [ 73%]
tests/test_validation_engine.py::test_email_validation PASSED            [ 78%]
tests/test_validation_engine.py::test_mobile_validation PASSED           [ 84%]
tests/test_validation_engine.py::test_pin_code_validation PASSED         [ 89%]
tests/test_validation_engine.py::test_aadhaar_validation PASSED          [ 94%]
tests/test_validation_engine.py::test_cross_check_mismatch PASSED        [100%]

======================= 19 passed in 6.36s =======================
```

**Status:** **19 Passed, 0 Failed (100% Pass Rate)**

---

## 6. How to Run the Application

### 1-Click Launch (Recommended)
From the workspace root directory:
```bash
python run_formpilot.py
```
- **Web Application:** `http://127.0.0.1:8000`
- **Swagger API Docs:** `http://127.0.0.1:8000/docs`
- **Health Check:** `http://127.0.0.1:8000/api/health`

### Running Backend Manually
```bash
cd formpilot-ai
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Running Frontend (Next.js)
```bash
cd formpilot-ai/frontend
npm install
npm run dev
```

---

## 7. Supabase & Cloud Deployment Configuration

### Supabase Setup
1. Create a project at [supabase.com](https://supabase.com).
2. Open the **SQL Editor** in the Supabase Dashboard.
3. Paste and run `formpilot-ai/supabase/schema.sql`. This creates the `profiles`, `documents`, `form_analyses`, `applications`, and `chat_messages` tables with Row Level Security (RLS) enabled.
4. Set `DATABASE_URL` in `.env` to your Supabase PostgreSQL connection string.

### Google OAuth Configuration
1. In Google Cloud Console, create OAuth 2.0 Client Credentials.
2. Add Authorized Redirect URI: `https://[YOUR-PROJECT-ID].supabase.co/auth/v1/callback`.
3. In Supabase Dashboard -> **Authentication -> Providers -> Google**, enable Google and enter the Client ID & Secret.

---

## 8. License & Acknowledgements
- Developed for **INNOVATE INDIA Hackathon 2026**.
- Presented by **Sarathkumar R (Team Davengers)**.
