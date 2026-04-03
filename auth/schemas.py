from pydantic import BaseModel, EmailStr
from typing import Optional

# ১. Base Schema (কমন ফিল্ডগুলো এখানে থাকবে)
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

# ২. Create Schema (ইউজার রেজিস্ট্রেশনের সময় যা যা রিকোয়েস্ট বডিতে আসবে)
class UserCreate(UserBase):
    password: str

# ৩. Response Schema (API থেকে ক্লায়েন্ট বা ফ্রন্টএন্ডকে যা ফেরত দেওয়া হবে)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # SQLAlchemy মডেল থেকে Pydantic মডেলে ডাটা কনভার্ট করার অনুমতি দেয়

# ৪. Token Schema (লগিন করার পর যে JWT টোকেন দেওয়া হবে)
class Token(BaseModel):
    access_token: str
    token_type: str