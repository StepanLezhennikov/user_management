from dataclasses import dataclass

from app.domain.base_entity import BaseDTO


@dataclass
class Role(BaseDTO):
    name: str
