from logging import getLogger

from pydantic import EmailStr

from app.core.config import Constants
from app.api.interfaces.services.email import AEmailService
from app.services.interfaces.clients.aws.email import AEmailClient

logger = getLogger(__name__)


class EmailService(AEmailService):
    def __init__(self, email_client: AEmailClient):
        self.email_client = email_client

    async def send_code(self, email: EmailStr, subject: str, code: int) -> bool:
        message = Constants.message_for_email + str(code)
        return await self.email_client.send_message(
            email=email, subject=subject, message=message
        )
