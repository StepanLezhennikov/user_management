import aioboto3
from pydantic import EmailStr

from app.core.config import settings
from app.infra.uow.uow import logger
from app.services.interfaces.clients.aws.email import AEmailClient


class EmailClient(AEmailClient):
    def __init__(self, aioboto3_session: aioboto3.Session):
        self._session = aioboto3_session

    async def send_message(self, email: EmailStr, subject: str, message: str) -> bool:
        async with self._session.client(
            "ses", endpoint_url=settings.AWS_ENDPOINT_URL
        ) as ses:
            result = await ses.send_email(
                Source=settings.AWS_EMAIL_SOURCE,
                Destination={"ToAddresses": [email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": message}},
                },
            )
            logger.debug("Email sent!")
            return bool(result)
