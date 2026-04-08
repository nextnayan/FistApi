from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    
    # ফরেন কী (Foreign Key) - কোন ইউজার এই প্রোডাক্টটি তৈরি করেছে
    owner_id = Column(Integer, ForeignKey("users.id"))

    # রিলেশনশিপ (যাতে প্রোডাক্ট থেকে সহজেই ইউজারের ডাটা পাওয়া যায়)
    owner = relationship("User")