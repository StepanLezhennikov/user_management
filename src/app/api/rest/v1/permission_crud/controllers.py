from fastapi import Query, Depends, APIRouter, HTTPException
from starlette import status
from dependency_injector.wiring import Provide, inject

from app.schemas.permission import (
    Permission,
    PermissionCreate,
    PermissionFilter,
    PermissionUpdate,
)
from app.services.services.permission import permission_required
from app.api.exceptions.permission_service import (
    PermissionsNotFoundError,
    PermissionAlreadyExistsError,
)
from app.api.interfaces.services.permission import APermissionService

router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(permission_required("permission_create"))],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_permission(
    permission_create: PermissionCreate,
    permission_service: APermissionService = Depends(Provide["permission_service"]),
) -> PermissionCreate:
    try:
        await permission_service.create(permission_create)
    except PermissionAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Permission already exists")
    return permission_create


@router.get("/", dependencies=[Depends(permission_required("permission_get"))])
@inject
async def get_permission(
    permission_filter: PermissionFilter = Query(None),
    permission_service: APermissionService = Depends(Provide["permission_service"]),
) -> list[Permission]:
    try:
        permissions = await permission_service.get(**(permission_filter.model_dump()))
    except PermissionsNotFoundError:
        raise HTTPException(status_code=404, detail="Permissions not found")

    return permissions


@router.put("/", dependencies=[Depends(permission_required("permission_update"))])
@inject
async def update_permission(
    permission_id: int,
    permission_update: PermissionUpdate,
    permission_service: APermissionService = Depends(Provide["permission_service"]),
) -> Permission:
    try:
        updated_permission = await permission_service.update(
            permission_id, permission_update
        )
    except PermissionsNotFoundError:
        raise HTTPException(status_code=404, detail="Permissions not found")

    return updated_permission


@router.delete("/", dependencies=[Depends(permission_required("permission_delete"))])
@inject
async def delete_permission(
    permission_id: int,
    permission_service: APermissionService = Depends(Provide["permission_service"]),
) -> Permission:
    try:
        deleted_permission = await permission_service.delete(permission_id)
    except PermissionsNotFoundError:
        raise HTTPException(status_code=404, detail="Permissions not found")

    return deleted_permission
