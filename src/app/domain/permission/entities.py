from enum import Enum
from dataclasses import dataclass

from app.domain.base_entity import BaseDTO


class PermissionName(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"


@dataclass
class Permission(BaseDTO):
    name: PermissionName
    description: str
