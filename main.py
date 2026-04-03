from fastapi import FastAPI
from core.config import settings
from core.database import engine, Base
from auth import router as auth_router

# FastAPI অ্যাপ ইনিশিয়ালাইজেশন
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# একটি বেসিক রুট (Health Check)
@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs_url": "Visit /docs for Swagger UI"
    }




# ডাটাবেসে আমাদের তৈরি করা মডেল (টেবিল) গুলো জেনারেট করা
Base.metadata.create_all(bind=engine)

# Auth রাউটারকে মূল অ্যাপের সাথে যুক্ত করা
app.include_router(auth_router.router)