from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.context import CryptContext
from core.config import settings

# ১. পাসওয়ার্ড হ্যাশিংয়ের জন্য কনটেক্সট তৈরি
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ২. পাসওয়ার্ড ভেরিফাই করার ফাংশন (লগিনের সময় লাগবে)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ইউজারের দেওয়া পাসওয়ার্ড এবং ডাটাবেসের হ্যাশ করা পাসওয়ার্ড মেলানোর জন্য"""
    return pwd_context.verify(plain_password, hashed_password)

# ৩. পাসওয়ার্ড হ্যাশ করার ফাংশন (রেজিস্ট্রেশনের সময় লাগবে)
def get_password_hash(password: str) -> str:
    """সাধারণ পাসওয়ার্ডকে এনক্রিপ্ট বা হ্যাশ করার জন্য"""
    return pwd_context.hash(password)

# ৪. JWT (JSON Web Token) তৈরি করার ফাংশন
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """ইউজার লগিন করলে তাকে একটি টোকেন দেওয়ার জন্য"""
    to_encode = data.copy()
    
    # টোকেনের মেয়াদ নির্ধারণ (Expiration Time)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # ডিফল্টভাবে টোকেনের মেয়াদ ১৫ মিনিট
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    
    # টোকেন জেনারেট করা (Secret Key ব্যবহার করে)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    
    return encoded_jwt