from fastapi import FastAPI
from core.config import settings

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