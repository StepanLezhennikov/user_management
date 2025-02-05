from logging import getLogger

import aioboto3
from pydantic import EmailStr

from app.core.config import settings
from app.api.interfaces.services.email_service import AEmailService

logger = getLogger(__name__)


class EmailService(AEmailService):

    def __init__(self, aioboto3_session: aioboto3.Session):
        self._session = aioboto3_session

    async def send_code(self, email: EmailStr, subject: str, code: int) -> None:
        async with self._session.client(
            "ses", endpoint_url=settings.AWS_ENDPOINT_URL
        ) as ses:
            await ses.send_email(
                Source=settings.AWS_EMAIL_SOURCE,
                Destination={"ToAddresses": [email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": f"Код подтверждения: {code}"}},
                },
            )
            logger.debug("Email sent! Code:", code)
