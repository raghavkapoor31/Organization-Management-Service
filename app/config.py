from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    master_db_name: str = "master_db"
    jwt_secret_key: str = "your-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    port: int = 8000
    
    # For production deployments, these will be set via environment variables
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

