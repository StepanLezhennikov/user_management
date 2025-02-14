import os
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


@dataclass
class Constants:
    subject_for_email: str = "Подтверждение почты"
    message_for_email: str = "Код подтверждения: "
    expiration_time_for_code: int = 300


class Settings(BaseSettings):
    DEBUG: bool = True

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")

    AWS_REGION_NAME: str = os.getenv("AWS_REGION_NAME")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_ENDPOINT_URL: str = os.getenv("AWS_ENDPOINT_URL")
    AWS_EMAIL_SOURCE: str = os.getenv("AWS_EMAIL_SOURCE")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        extra = "allow"


settings = Settings()
