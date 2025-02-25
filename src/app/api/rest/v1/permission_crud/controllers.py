from fastapi import APIRouter
from dependency_injector.wiring import inject

from app.schemas.permission import PermissionCreate

router = APIRouter()


@router.post("/")
@inject
async def create_permission(
    permission_create: PermissionCreate,
) -> PermissionCreate:
    return permission_create


@router.get("/")
@inject
async def get_permission(
    permission_create: PermissionCreate,
) -> PermissionCreate:
    return permission_create


@router.put("/")
@inject
async def update_permission(
    permission_create: PermissionCreate,
) -> PermissionCreate:
    return permission_create


@router.delete("/")
@inject
async def delete_permission(
    permission_create: PermissionCreate,
) -> PermissionCreate:
    return permission_create
