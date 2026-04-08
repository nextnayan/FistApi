import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.config import settings
from core.database import get_db
from auth import service, models

# ১. OAuth2 স্কিমা সেটআপ (FastAPI-কে বলে দেওয়া যে আমাদের লগিন URL কোনটি)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ২. বর্তমান লগিন করা ইউজারকে বের করার ফাংশন
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """ফ্রন্টএন্ড থেকে আসা টোকেনটি যাচাই করে আসল ইউজারকে ডাটাবেস থেকে খুঁজে বের করে"""
    
    # যদি টোকেন ভুল হয় বা মেয়াদ শেষ হয়ে যায়, তবে এই এররটি দেখাবো
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="আপনার টোকেনটি সঠিক নয় অথবা মেয়াদ শেষ হয়ে গেছে। দয়া করে আবার লগিন করুন।",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Secret Key দিয়ে টোকেনটিকে আনলক বা ডিকোড করছি
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub") # লগিন করার সময় আমরা 'sub' এর ভেতরে ইমেইল রেখেছিলাম
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    # ইমেইল পেয়ে গেলে ডাটাবেস থেকে ইউজারকে খুঁজছি
    user = service.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
        
    return user