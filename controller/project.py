from typing import Optional

from fastapi import APIRouter, Path, Query
from starlette.requests import Request

from common.auth import permission_required
from enums.common_enum import OperationTypeEnum
from enums.user_enum import UserRoleEnum
from common.r import R
from common.write_log import log
from config.configure import settings
from schemas.project_schema import ProjectAddSchema, ProjectResponseSchema, ProjectUpdateSchema
from service.project_service import project_service

project_router = APIRouter(prefix=settings.PATH_PREFIX + "/projects",tags=["项目"])


@project_router.post("", response_model=ProjectResponseSchema)
@log(OperationTypeEnum.PROJECT_ADD.value)
@permission_required(role=UserRoleEnum.ADMIN.value)
def add(project_schema: ProjectAddSchema, request: Request = None):
    project = project_service.add_project(project_schema=project_schema, current_user=request.current_user)
    return R.ok(data=project)


@project_router.put("/{_id}")
@log(OperationTypeEnum.PROJECT_UPDATE.value)
@permission_required(role=UserRoleEnum.ADMIN.value)
def update(*, _id: int = Path(None), project_schema: ProjectUpdateSchema, request: Request = None):
    project = project_service.update_project(_id=_id, project_schema=project_schema, current_user=request.current_user)
    return R.ok(data=project)


@project_router.get("/all")
@permission_required()
def get_all(request: Request = None):
    projects = project_service.get_all_project()
    return R.ok(data=projects)


@project_router.get("")
@permission_required()
def get_by_page(current_page: Optional[int] = 1,
                page_size: Optional[int] = 20,
                name: Optional[str] = Query(default=""),
                type: Optional[str] = Query(default=""),
                request: Request = None):
    total, projects = project_service.get_projects_by_page(current_page=current_page, page_size=page_size,
                                                           name=name, type=type)
    return R.ok(data=dict(total=total, list=projects))


@project_router.delete("/{_id}")
@log(OperationTypeEnum.PROJECT_DELETE.value)
@permission_required()
def delete_by_id(_id: int = Path(default=0), request: Request = None):
    project_service.delete_project_by_id(_id=_id)
    return R.ok(message="删除项目成功")


@project_router.get("/{_id}")
@permission_required()
def get_by_id(_id: int = Path(default=0), request: Request = None):
    project = project_service.get_project_by_id(_id=_id)
    return R.ok(data=project)
