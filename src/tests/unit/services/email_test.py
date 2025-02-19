from pydantic import EmailStr

from app.services.services.email import EmailService


async def test_send_code(
    email_service: EmailService, email: EmailStr, code: int
) -> None:
    assert await email_service.send_code(email=email, code=code)
