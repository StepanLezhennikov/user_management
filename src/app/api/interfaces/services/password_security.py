from abc import ABC, abstractmethod


class APasswordSecurityService(ABC):
    @abstractmethod
    def verify_password(self, password: str, stored_password: str) -> bool:
        pass

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass
