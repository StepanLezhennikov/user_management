import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool = True

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")

    AWS__REGION_NAME: str = os.getenv("AWS__REGION_NAME")
    AWS__ACCESS_KEY_ID: str = os.getenv("AWS__ACCESS_KEY_ID")
    AWS__SECRET_ACCESS_KEY: str = os.getenv("AWS__SECRET_ACCESS_KEY")
    AWS__ENDPOINT_URL: str = os.getenv("AWS__ENDPOINT_URL")
    AWS__EMAIL_SOURCE: str = os.getenv("AWS__EMAIL_SOURCE")

    class Config:
        extra = "allow"


settings = Settings()
