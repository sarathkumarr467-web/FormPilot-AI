"""
Application Tracker API for FormPilot AI.
Provides full CRUD for tracking applications, deadlines, statuses, checklists, and reminders.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.application import Application
from ..schemas.schemas import ApplicationCreate, ApplicationUpdate, ApplicationResponse

router = APIRouter(prefix="/applications", tags=["Applications"])

DEFAULT_CHECKLIST = [
    {"item": "Identity Proof (Aadhaar Card)", "done": True, "required": True},
    {"item": "Income Certificate from Tahsildar", "done": True, "required": True},
    {"item": "Community / Caste Certificate", "done": True, "required": True},
    {"item": "College Bonafide Certificate", "done": False, "required": True},
    {"item": "Previous Year Marksheet", "done": True, "required": True},
    {"item": "Bank Passbook Copy (DBT Linked)", "done": True, "required": True}
]

@router.get("", response_model=List[ApplicationResponse])
def get_applications(user_id: int = 1, db: Session = Depends(get_db)):
    apps = db.query(Application).filter(Application.user_id == user_id).order_by(Application.created_at.desc()).all()
    if not apps:
        # Seed realistic initial applications if user has none
        seed_apps = [
            Application(
                user_id=user_id,
                title="Post-Matric Scholarship Scheme 2026-27",
                category="Scholarship",
                deadline="2026-12-15",
                status="In Progress",
                progress_percent=65,
                portal_url="https://scholarships.gov.in",
                notes="College verification pending. Met with nodal officer on Monday.",
                checklist=DEFAULT_CHECKLIST,
                reminder_date="2026-11-25"
            ),
            Application(
                user_id=user_id,
                title="TNEA Anna University Engineering Counseling",
                category="College Admission",
                deadline="2026-07-20",
                status="Completed",
                progress_percent=100,
                portal_url="https://www.tneaonline.org",
                notes="Allotment order downloaded and accepted.",
                checklist=[{"item": "12th Marksheet", "done": True, "required": True}, {"item": "TC", "done": True, "required": True}],
                reminder_date=""
            ),
            Application(
                user_id=user_id,
                title="TCS Smart Hiring / GET 2026",
                category="Job Application",
                deadline="2026-12-30",
                status="Ready for Review",
                progress_percent=85,
                portal_url="https://ibegin.tcs.com",
                notes="Resume verified with FormPilot. Prepared for aptitude test.",
                checklist=[{"item": "Resume PDF", "done": True, "required": True}, {"item": "Degree Certificate", "done": True, "required": True}],
                reminder_date="2026-12-01"
            )
        ]
        for a in seed_apps:
            db.add(a)
        db.commit()
        apps = seed_apps

    return [
        {
            "id": a.id,
            "title": a.title,
            "category": a.category,
            "deadline": a.deadline,
            "status": a.status,
            "progress_percent": a.progress_percent,
            "portal_url": a.portal_url,
            "notes": a.notes,
            "checklist": a.checklist or [],
            "reminder_date": a.reminder_date,
            "created_at": a.created_at.strftime("%Y-%m-%d")
        }
        for a in apps
    ]

@router.post("", response_model=ApplicationResponse)
def create_application(app_in: ApplicationCreate, user_id: int = 1, db: Session = Depends(get_db)):
    checklist = app_in.checklist if app_in.checklist is not None else DEFAULT_CHECKLIST
    new_app = Application(
        user_id=user_id,
        title=app_in.title,
        category=app_in.category,
        deadline=app_in.deadline,
        status=app_in.status,
        progress_percent=app_in.progress_percent,
        portal_url=app_in.portal_url,
        notes=app_in.notes or "",
        checklist=checklist,
        reminder_date=app_in.reminder_date
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return {
        "id": new_app.id,
        "title": new_app.title,
        "category": new_app.category,
        "deadline": new_app.deadline,
        "status": new_app.status,
        "progress_percent": new_app.progress_percent,
        "portal_url": new_app.portal_url,
        "notes": new_app.notes,
        "checklist": new_app.checklist or [],
        "reminder_date": new_app.reminder_date,
        "created_at": new_app.created_at.strftime("%Y-%m-%d")
    }

@router.put("/{app_id}", response_model=ApplicationResponse)
def update_application(app_id: int, app_in: ApplicationUpdate, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")

    if app_in.title is not None: app.title = app_in.title
    if app_in.category is not None: app.category = app_in.category
    if app_in.deadline is not None: app.deadline = app_in.deadline
    if app_in.status is not None: app.status = app_in.status
    if app_in.progress_percent is not None: app.progress_percent = app_in.progress_percent
    if app_in.portal_url is not None: app.portal_url = app_in.portal_url
    if app_in.notes is not None: app.notes = app_in.notes
    if app_in.checklist is not None: app.checklist = app_in.checklist
    if app_in.reminder_date is not None: app.reminder_date = app_in.reminder_date

    db.commit()
    db.refresh(app)
    return {
        "id": app.id,
        "title": app.title,
        "category": app.category,
        "deadline": app.deadline,
        "status": app.status,
        "progress_percent": app.progress_percent,
        "portal_url": app.portal_url,
        "notes": app.notes,
        "checklist": app.checklist or [],
        "reminder_date": app.reminder_date,
        "created_at": app.created_at.strftime("%Y-%m-%d")
    }

@router.delete("/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found.")
    db.delete(app)
    db.commit()
    return {"success": True, "message": "Application deleted successfully."}
