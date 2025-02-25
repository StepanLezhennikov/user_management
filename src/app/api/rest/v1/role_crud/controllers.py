from fastapi import APIRouter
from dependency_injector.wiring import inject

from app.schemas.role import RoleCreate

router = APIRouter()


@router.post("/")
@inject
async def create_role(
    role_create: RoleCreate,
) -> RoleCreate:
    return role_create


@router.get("/")
@inject
async def get_role(
    role_create: RoleCreate,
) -> RoleCreate:
    return role_create


@router.put("/")
@inject
async def update_role(
    role_create: RoleCreate,
) -> RoleCreate:
    return role_create


@router.delete("/")
@inject
async def delete_role(
    role_create: RoleCreate,
) -> RoleCreate:
    return role_create
