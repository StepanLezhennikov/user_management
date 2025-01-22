from sqlalchemy.orm import declarative_base

Base = declarative_base()

from src.app.models.user import User
