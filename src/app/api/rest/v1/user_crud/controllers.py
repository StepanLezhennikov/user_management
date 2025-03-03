from fastapi import Query, Depends, APIRouter, HTTPException
from starlette import status
from dependency_injector.wiring import Provide, inject

from app.schemas.user import (
    User,
    UserCreate,
    UserUpdate,
    DeletedUser,
    UserAuthenticated,
)
from app.services.services.jwt import get_current_user
from app.api.exceptions.user_service import (
    UserNotFoundError,
    UserIsAlreadyRegisteredError,
)
from app.api.interfaces.services.user import AUserService
from app.services.services.permission import permission_required

router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(permission_required("user_create"))],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_user(
    user_create: UserCreate,
    user_service: AUserService = Depends(Provide["user_service"]),
) -> User:
    try:
        created_user = await user_service.create(user_create)
    except UserIsAlreadyRegisteredError:
        raise HTTPException(status_code=409, detail="User already exists")
    return created_user


@router.get(
    "/",
    dependencies=[Depends(permission_required("user_get"))],
)
@inject
async def get_users(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_service: AUserService = Depends(Provide["user_service"]),
) -> list[User]:
    try:
        users = await user_service.get_all(limit=limit, offset=offset)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    return users


@router.put("/")
@inject
async def update_me(
    user_update: UserUpdate,
    current_user: UserAuthenticated = Depends(get_current_user),
    user_service: AUserService = Depends(Provide["user_service"]),
) -> User:
    try:
        updated_user = await user_service.update(current_user.id, user_update)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.delete("/")
@inject
async def delete_me(
    current_user: UserAuthenticated = Depends(get_current_user),
    user_service: AUserService = Depends(Provide["user_service"]),
) -> DeletedUser:
    try:
        deleted_user = await user_service.delete(current_user.id)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    return deleted_user
