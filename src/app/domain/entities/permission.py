from dataclasses import dataclass
from uuid import UUID

from src.app.domain.entities.base import BaseMixin


@dataclass
class Permission(BaseMixin):
    name: str
    description: str
    role_id: UUID