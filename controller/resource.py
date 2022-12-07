from typing import Optional

from fastapi import APIRouter, Path, Query, Body
from starlette.requests import Request

from common.auth import permission_required
from enums.common_enum import OperationTypeEnum
from enums.resource_enum import ResourceCategoryEnum
from enums.user_enum import UserRoleEnum
from common.r import R
from common.write_log import log
from config.configure import settings
from schemas.resource_schema import ResourceTypeAddSchema, ResourceTypeUpdateSchema, ResourceHttpAddSchema, \
    ResourceShellAddSchema, ResourceDatabaseAddSchema, ResourceHttpUpdateSchema, ResourceShellUpdateSchema, \
    ResourceDatabaseUpdateSchema
from service.resource_service import resource_service

resource_router = APIRouter(prefix=settings.PATH_PREFIX + "/resources")


@resource_router.post("/types")
@log(OperationTypeEnum.RESOURCE_TYPE_ADD.value)
@permission_required(UserRoleEnum.ADMIN.value)
def add_resource_type(schema: ResourceTypeAddSchema, request: Request = None):
    """
    添加资源类型
    :param schema:
    :param request:
    :return:
    """
    new_resource_type = resource_service.add_resource_type(schema=schema, current_user=request.current_user)
    return R.ok(data=new_resource_type)


@resource_router.put("/types/{_id}")
@log(OperationTypeEnum.RESOURCE_TYPE_UPDATE.value)
@permission_required(UserRoleEnum.ADMIN.value)
def update_resource_type(*, _id: int = Path(None),
                         schema: ResourceTypeUpdateSchema,
                         request: Request = None):
    """
    更新资源类型
    :param _id:资源id
    :param schema:
    :param request:
    :return:
    """
    new_resource_type = resource_service.update_resource_type_by_id(
        _id=_id,
        schema=schema,
        current_user=request.current_user
    )
    return R.ok(data=new_resource_type)


@resource_router.delete("/types/{_id}")
@log(OperationTypeEnum.RESOURCE_TYPE_DELETE.value)
@permission_required(UserRoleEnum.ADMIN.value)
def delete_resource_type(*, _id: int,
                         request: Request = None):
    """
    删除资源类型
    :param _id: 资源id
    :param request:
    :return:
    """
    resource_service.delete_resource_type_by_id(_id=_id)
    return R.ok(message="删除资源类型成功")


@resource_router.get("/types/all")
@permission_required(UserRoleEnum.ADMIN.value)
def get_all_resource_type(
        project_id: int = Query(default=None),
        category: str = Query(default=None),
        request: Request = None
):
    """
    根据项目ID和类别获取资源类型
    :param project_id: 项目ID
    :param category: 类别：http、shell、database等
    :param request:
    :return:
    """
    resource_type_list = resource_service.get_all_resource_type(project_id=project_id, category=category)
    return R.ok(data=resource_type_list)


@resource_router.post("")
@log(OperationTypeEnum.RESOURCE_ADD.value)
@permission_required()
def add_resource(http: Optional[ResourceHttpAddSchema] = None,
                 shell: Optional[ResourceShellAddSchema] = None,
                 database: Optional[ResourceDatabaseAddSchema] = None,
                 category: ResourceCategoryEnum = Body(..., embed=True),
                 request: Request = None):
    """
    添加http类型的资源
    :param http:
    :param shell:
    :param database:
    :param request:
    :param category:
    :return:
    """
    if category == ResourceCategoryEnum.HTTP.value and not http:
        return R.error(message="Http不可为空")
    if category == ResourceCategoryEnum.SHELL.value and not shell:
        return R.error(message="Shell不可为空")
    if category == ResourceCategoryEnum.DATABASE.value and not database:
        return R.error(message="Database不可为空")

    resource = resource_service.add_resource(
        http=http,
        shell=shell,
        database=database,
        category=category,
        current_user=request.current_user)
    return R.ok(data=resource, message="新增资源成功")


@resource_router.put("/{_id}")
@log(OperationTypeEnum.RESOURCE_UPDATE.value)
@permission_required()
def update_resource(_id=Path(default=0),
                    http: Optional[ResourceHttpUpdateSchema] = None,
                    shell: Optional[ResourceShellUpdateSchema] = None,
                    database: Optional[ResourceDatabaseUpdateSchema] = None,
                    category: ResourceCategoryEnum = Body(..., embed=True),
                    request: Request = None):
    """
    更新http类型的资源
    :param _id:
    :param http:
    :param shell:
    :param database:
    :param request:
    :param category:
    :return:
    """
    if category == ResourceCategoryEnum.HTTP.value and not http:
        return R.error(message="Http不可为空")
    if category == ResourceCategoryEnum.SHELL.value and not shell:
        return R.error(message="Shell不可为空")
    if category == ResourceCategoryEnum.DATABASE.value and not database:
        return R.error(message="Database不可为空")

    resource = resource_service.update_resource(
        _id=_id,
        http=http,
        shell=shell,
        database=database,
        category=category,
        current_user=request.current_user)
    return R.ok(data=resource, message="更新资源成功")


@resource_router.delete("/{_id}")
@log(OperationTypeEnum.RESOURCE_DELETE.value)
@permission_required()
def delete_resource(*, _id: int = Path(None), category: str, request: Request = None):
    resource_service.delete_resource(_id=_id, category=category)
    return R.ok(message="删除资源成功")


@resource_router.get("")
@permission_required()
def get_resources_by_page(
        *,
        current_page: Optional[int] = 1,
        page_size: Optional[int] = 20,
        name: Optional[str] = Query(default=""),
        project_id: int = Query(default=0),
        category: str,
        request:Request=None
):
    total, resources = resource_service.get_resources_by_page(current_page=current_page,
                                                              page_size=page_size,
                                                              name=name,
                                                              project_id=project_id,
                                                              category=category)
    return R.ok(data=dict(total=total, list=resources))


@resource_router.get("/all")
@permission_required()
def get_all_resource(*, project_id: int, request: Request = None):
    """

    :param project_id:
    :param request:
    :return:
    """
    resources = resource_service.get_all_resource_by_category(project_id=project_id)
    return R.ok(data=resources)
