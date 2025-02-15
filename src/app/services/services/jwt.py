# from datetime import datetime, timedelta
# from typing import Union
# from pyjwt import jwt
# from dotenv import load_dotenv
#
# from fastapi import HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
#
# from app.core.config import settings
#
# load_dotenv()
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
#
#
# def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
#     to_encode = data.copy()
#     expire = datetime.now() + (
#         expires_delta
#         if expires_delta
#         else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     )
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
#     )
#     return encoded_jwt
#
#
# def verify_token(token: str):
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
#         )
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")
#
#
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     payload = verify_token(token)
#     return payload  # Вернуть можно и username или другие данные
