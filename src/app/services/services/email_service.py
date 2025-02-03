import aioboto3
from botocore.exceptions import BotoCoreError, ClientError

from app.api.interfaces.services.email_service import AEmailService
from app.core.config import settings


class SesClient:
    def __init__(self):
        self.session = aioboto3.Session(
            aws_access_key_id=settings.AWS__ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS__SECRET_ACCESS_KEY,
            region_name=settings.AWS__REGION_NAME,
        )


ses_client = SesClient()


class EmailService(AEmailService):
    async def send_message(self, email: str, subject: str, message: str) -> bool:
        async with ses_client.session.client(
            "ses",
            endpoint_url=settings.AWS__ENDPOINT_URL,
        ) as ses:
            try:
                ses.send_email(
                    Source=settings.AWS__EMAIL_SOURCE,
                    Destination={"ToAddresses": [email]},
                    Message={"Subject": subject, "Body": message},
                )
            except (BotoCoreError, ClientError) as e:
                print(e)
                return False
        return True
