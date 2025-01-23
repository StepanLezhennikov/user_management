from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from src.app.domain.entities.base import BaseMixin

class PermissionName(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"


@dataclass
class Permission(BaseMixin):
    name: PermissionName
    description: str