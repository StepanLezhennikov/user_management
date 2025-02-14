from pydantic import EmailStr, BaseModel


class Code(BaseModel):
    code: int


class CodeVerification(Code):
    email: EmailStr
