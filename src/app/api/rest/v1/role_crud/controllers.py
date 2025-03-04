from fastapi import Query, Depends, APIRouter, HTTPException
from starlette import status
from dependency_injector.wiring import Provide, inject

from app.schemas.role import Role, RoleCreate, RoleFilter, RoleUpdate
from app.api.exceptions.role_service import RoleNotFoundError, RoleAlreadyExistsError
from app.api.interfaces.services.role import ARoleService
from app.services.services.permission import permission_required

router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(permission_required("role_create"))],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_role(
    role_create: RoleCreate,
    role_service: ARoleService = Depends(Provide["role_service"]),
) -> RoleCreate:
    try:
        await role_service.create(role_create)
    except RoleAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Role already exists"
        )
    return role_create


@router.get(
    "/",
    dependencies=[Depends(permission_required("role_get"))],
)
@inject
async def get_role(
    role_filter: RoleFilter = Query(default=None),
    role_service: ARoleService = Depends(Provide["role_service"]),
) -> list[Role]:
    try:
        roles = await role_service.get(**(role_filter.model_dump()))
    except RoleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    return roles


@router.put("/", dependencies=[Depends(permission_required("role_update"))])
@inject
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    role_service: ARoleService = Depends(Provide["role_service"]),
) -> Role:
    try:
        updated_role = await role_service.update(role_id, role_update)
    except RoleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    return updated_role


@router.delete("/", dependencies=[Depends(permission_required("role_delete"))])
@inject
async def delete_role(
    role_id: int,
    role_service: ARoleService = Depends(Provide["role_service"]),
) -> Role:
    try:
        deleted_role = await role_service.delete(role_id)
    except RoleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    return deleted_role
