from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# ১. ডাটাবেস ইঞ্জিন তৈরি (SQLAlchemy-এর সাথে ডাটাবেসের মূল কানেকশন)
# নোট: SQLite-এর জন্য connect_args={"check_same_thread": False} লাগে, PostgreSQL বা MySQL-এ এটি লাগে না।
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# ২. সেশন মেকার (ডাটাবেসের সাথে কথা বলার জন্য একটি সেশন বা ওয়ার্কস্পেস)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ৩. বেস ক্লাস (আমাদের সব ডাটাবেস মডেল বা টেবিল এই ক্লাসটিকে ইনহেরিট করবে)
Base = declarative_base()

# ৪. ডাটাবেস ডিপেন্ডেন্সি (Best Practice)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()