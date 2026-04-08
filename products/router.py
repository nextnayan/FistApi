from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from auth.models import User
from auth.utils import get_current_user
from products import schemas, service

# রাউটার ইনিশিয়ালাইজেশন
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# ১. নতুন প্রোডাক্ট তৈরি (শুধু লগিন করা ইউজাররাই পারবে)
@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas.ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 🔒 সিকিউরিটি লেয়ার বা পাহারাদার
):
    """লগিন করা অবস্থায় নতুন প্রোডাক্ট তৈরি করার জন্য"""
    # current_user.id স্বয়ংক্রিয়ভাবে টোকেন থেকে আইডি বের করে নেবে
    return service.create_product(db=db, product=product, user_id=current_user.id)

# ২. সব প্রোডাক্ট দেখা (যে কেউ দেখতে পারবে, লগিন লাগবে না)
@router.get("/", response_model=list[schemas.ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ডাটাবেসের সব প্রোডাক্টের লিস্ট দেখার জন্য"""
    return service.get_products(db, skip=skip, limit=limit)