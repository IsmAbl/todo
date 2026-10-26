import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    allowed_origins: list[str]

def get_settings() -> Settings:
    cors_env = os.getenv("ALLOWED_ORIGIN")
    cors_list = [origin.strip() for origin in cors_env.split(",")]
    return Settings(
        DATABASE_URL=os.getenv("DATABASE_URL"), 
        allowed_origins=cors_list,
    )