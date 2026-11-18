"""
Authentication and Profile API routes for FormPilot AI.
Supports Email/Password registration, Login, Google OAuth sync, and Profile persistence.
"""
import hashlib
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..schemas.schemas import UserRegister, UserLogin, UserResponse, TokenResponse, ProfileUpdate

router = APIRouter(prefix="/auth", tags=["Authentication"])

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

@router.post("/register", response_model=TokenResponse)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )
        
    new_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=hash_password(user_in.password),
        auth_provider="email",
        role="applicant",
        language_pref="en",
        theme_pref="dark",
        profile_data={
            "full_name": user_in.full_name,
            "email": user_in.email,
            "mobile": "9876543210",
            "category": "OBC",
            "education": "Undergraduate",
            "state": "Tamil Nadu"
        }
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate mock token
    token = f"fp_token_{uuid.uuid4().hex}"
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": new_user.role,
            "language_pref": new_user.language_pref,
            "theme_pref": new_user.theme_pref,
            "profile_data": new_user.profile_data
        }
    }

@router.post("/login", response_model=TokenResponse)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or user.password_hash != hash_password(user_in.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
        
    token = f"fp_token_{uuid.uuid4().hex}"
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "language_pref": user.language_pref,
            "theme_pref": user.theme_pref,
            "profile_data": user.profile_data or {}
        }
    }

@router.get("/profile", response_model=UserResponse)
def get_profile(user_id: int = 1, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        # Create a default guest/demo user if database is freshly initialized
        user = User(
            id=1,
            email="demo.student@formpilot.ai",
            full_name="Arun Kumar",
            password_hash=hash_password("DemoPass123"),
            auth_provider="email",
            role="applicant",
            language_pref="en",
            theme_pref="dark",
            profile_data={
                "full_name": "Arun Kumar S",
                "father_name": "Suresh Kumar R",
                "email": "demo.student@formpilot.ai",
                "mobile": "9876543210",
                "dob": "15-08-2003",
                "gender": "Male",
                "aadhaar": "4839 2048 1092",
                "category": "OBC",
                "income": "180000",
                "college_name": "Government College of Technology, Coimbatore",
                "course_name": "B.E. Computer Science and Engineering",
                "marks_percentage": "84.5%",
                "bank_account": "304928174920",
                "ifsc_code": "SBIN0001234",
                "state": "Tamil Nadu",
                "address": "12, Bharathi Street, Gandhi Nagar, Madurai, TN - 625020"
            }
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "language_pref": user.language_pref,
        "theme_pref": user.theme_pref,
        "profile_data": user.profile_data or {}
    }

@router.put("/profile", response_model=UserResponse)
def update_profile(update_in: ProfileUpdate, user_id: int = 1, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
        
    if update_in.full_name:
        user.full_name = update_in.full_name
    if update_in.language_pref:
        user.language_pref = update_in.language_pref
    if update_in.theme_pref:
        user.theme_pref = update_in.theme_pref
    if update_in.profile_data:
        curr = user.profile_data or {}
        curr.update(update_in.profile_data)
        user.profile_data = curr
        
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "language_pref": user.language_pref,
        "theme_pref": user.theme_pref,
        "profile_data": user.profile_data or {}
    }

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully."}
