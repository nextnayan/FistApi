from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

# এই settings অবজেক্টটি আমরা পুরো প্রজেক্টে ব্যবহার করব
settings = Settings()