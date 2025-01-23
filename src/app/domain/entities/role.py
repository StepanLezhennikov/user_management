from dataclasses import dataclass

from src.app.domain.entities.base import BaseMixin


@dataclass
class Role(BaseMixin):
    name: str
