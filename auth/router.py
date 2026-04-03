from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import create_access_token
from auth import schemas, service

# ১. রাউটার ইনিশিয়ালাইজেশন
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# ২. রেজিস্ট্রেশন এন্ডপয়েন্ট (POST /auth/register)
@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """নতুন ইউজার একাউন্ট তৈরি করার জন্য"""
    # প্রথমে চেক করব এই ইমেইলে আগে থেকেই কোনো একাউন্ট আছে কিনা
    db_user = service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="এই ইমেইল দিয়ে ইতোমধ্যে একটি একাউন্ট খোলা হয়েছে।"
        )
    # সব ঠিক থাকলে নতুন ইউজার তৈরি করব
    return service.create_user(db=db, user=user)

# ৩. লগিন এন্ডপয়েন্ট (POST /auth/login)
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ইমেইল ও পাসওয়ার্ড দিয়ে লগিন করে টোকেন নেওয়ার জন্য"""
    # ইউজার ভেরিফাই করা (নোট: form_data.username এখানে আমাদের ইমেইল হিসেবে কাজ করবে)
    user = service.authenticate_user(db, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ইমেইল অথবা পাসওয়ার্ড ভুল হয়েছে!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # সব ঠিক থাকলে একটি এক্সেস টোকেন (JWT) তৈরি করা
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}