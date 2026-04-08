from sqlalchemy.orm import Session
from products.models import Product
from products.schemas import ProductCreate

# ১. নতুন প্রোডাক্ট তৈরি করার ফাংশন
def create_product(db: Session, product: ProductCreate, user_id: int):
    """ইউজারের দেওয়া ডাটা এবং লগিন করা ইউজারের আইডি দিয়ে ডাটাবেসে প্রোডাক্ট সেভ করে"""
    
    # Pydantic মডেলের ডাটাগুলোকে ডিকশনারিতে কনভার্ট করে ডাটাবেস মডেলে পাস করা হচ্ছে
    db_product = Product(**product.model_dump(), owner_id=user_id)
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product

# ২. সব প্রোডাক্ট লিস্ট আকারে দেখার ফাংশন (Pagination সহ)
def get_products(db: Session, skip: int = 0, limit: int = 100):
    """ডাটাবেস থেকে একাধিক প্রোডাক্টের লিস্ট নিয়ে আসে"""
    return db.query(Product).offset(skip).limit(limit).all()

# ৩. নির্দিষ্ট একটি প্রোডাক্ট দেখার ফাংশন
def get_product_by_id(db: Session, product_id: int):
    """আইডি দিয়ে নির্দিষ্ট একটি প্রোডাক্ট খুঁজে বের করে"""
    return db.query(Product).filter(Product.id == product_id).first()