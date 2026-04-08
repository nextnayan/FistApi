from pydantic import BaseModel
from typing import Optional

# ১. Base Schema (কমন ফিল্ডগুলো এখানে থাকবে)
class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float

# ২. Create Schema (প্রোডাক্ট তৈরি করার সময় ফ্রন্টএন্ড থেকে যা আসবে)
class ProductCreate(ProductBase):
    pass  # Base-এর ফিল্ডগুলোই যথেষ্ট, তাই নতুন কিছু যোগ করিনি

# ৩. Response Schema (ডাটাবেস থেকে প্রোডাক্ট রিড করে ফ্রন্টএন্ডে যা পাঠানো হবে)
class ProductResponse(ProductBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # ডাটাবেস অবজেক্টকে JSON-এ কনভার্ট করার জন্য