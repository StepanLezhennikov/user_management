from fastapi import Query, Depends, APIRouter, HTTPException
from starlette import status
from dependency_injector.wiring import Provide, inject

from app.schemas.user import User, UserCreate
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


#
# @router.put("/", dependencies=[Depends(permission_required("role_update"))])
# @inject
# async def update_role(
#     role_id: int,
#     role_update: RoleUpdate,
#     role_service: ARoleService = Depends(Provide["role_service"]),
# ) -> Role:
#     try:
#         updated_role = await role_service.update(role_id, role_update)
#     except RoleNotFoundError:
#         raise HTTPException(status_code=404, detail="Role not found")
#
#     return updated_role
#
#
# @router.delete("/", dependencies=[Depends(permission_required("role_delete"))])
# @inject
# async def delete_role(
#     role_id: int,
#     role_service: ARoleService = Depends(Provide["role_service"]),
# ) -> Role:
#     try:
#         deleted_role = await role_service.delete(role_id)
#     except RoleNotFoundError:
#         raise HTTPException(status_code=404, detail="Role not found")
#
#     return deleted_role
