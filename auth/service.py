from sqlalchemy.orm import Session
from auth.models import User
from auth.schemas import UserCreate
from core.security import get_password_hash, verify_password

# ১. ইমেইল দিয়ে ইউজার খোঁজার ফাংশন
def get_user_by_email(db: Session, email: str):
    """ডাটাবেসে এই ইমেইল দিয়ে কোনো একাউন্ট আছে কিনা তা চেক করে"""
    return db.query(User).filter(User.email == email).first()

# ২. নতুন ইউজার তৈরি (Registration) করার ফাংশন
def create_user(db: Session, user: UserCreate):
    """ইউজারের ডাটা নিয়ে পাসওয়ার্ড হ্যাশ করে ডাটাবেসে সেভ করে"""
    # ইউজারের দেওয়া পাসওয়ার্ডটি হ্যাশ করে নিচ্ছি
    hashed_password = get_password_hash(user.password)
    
    # ডাটাবেসের মডেল অনুযায়ী একটি নতুন ইউজার অবজেক্ট তৈরি
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    
    # ডাটাবেসে এড এবং সেভ (Commit) করা
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # ডাটাবেস থেকে নতুন তৈরি হওয়া ইউজারের আইডি (ID) নিয়ে আসার জন্য
    
    return db_user

# ৩. ইউজার লগিন (Authentication) করার ফাংশন
def authenticate_user(db: Session, email: str, password: str):
    """লগিনের সময় ইমেইল ও পাসওয়ার্ড সঠিক কিনা তা যাচাই করে"""
    # প্রথমে ইমেইল দিয়ে ইউজারকে খুঁজছি
    user = get_user_by_email(db, email)
    if not user:
        return False
    
    # এবার পাসওয়ার্ড মিলিয়ে দেখছি
    if not verify_password(password, user.hashed_password):
        return False
        
    return user