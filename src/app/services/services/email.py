from logging import getLogger

from pydantic import EmailStr

from app.core.config import Constants
from app.api.interfaces.services.email import AEmailService
from app.services.interfaces.clients.aws.email import AEmailClient

logger = getLogger(__name__)


class EmailService(AEmailService):
    def __init__(self, email_client: AEmailClient):
        self.email_client = email_client

    async def send_code(self, email: EmailStr, code: int) -> bool:
        message = Constants.message_for_code_sending_email.format(code=str(code))
        return await self.email_client.send_message(
            email=email,
            subject=Constants.subject_for_code_sending_email,
            message=message,
        )

    async def send_password_reset_link(self, email: EmailStr, token: str) -> bool:
        message = Constants.message_for_password_reset_email.format(
            password_token=token
        )
        print("Отправленное сообщение:", message)
        return await self.email_client.send_message(
            email=email,
            subject=Constants.subject_for_password_reset_email,
            message=message,
        )
