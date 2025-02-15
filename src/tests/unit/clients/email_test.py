from pydantic import EmailStr

from app.infra.clients.aws.email import EmailClient


async def test_send_message(email_client: EmailClient, email: EmailStr):
    assert await email_client.send_message(
        email=email,
        subject="Test",
        message="Test message",
    )
