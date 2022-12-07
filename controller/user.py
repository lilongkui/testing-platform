from typing import Optional

from fastapi import APIRouter, Path, Query
from starlette.requests import Request

from common.auth import permission_required
from enums.common_enum import OperationTypeEnum
from enums.user_enum import UserRoleEnum
from common.r import R
from common.write_log import log
from config.configure import settings
from schemas.user_schema import UserAddSchema, UserUpdateSchema, UserLoginSchema
from service.user_service import user_service

user_router = APIRouter(prefix=settings.PATH_PREFIX + "/users")


@user_router.post("")
@log(OperationTypeEnum.ADMIN_USER_ADD.value)
@permission_required(UserRoleEnum.ADMIN.value)
def add(user_schema: UserAddSchema, request: Request = None):
    """
    添加用户
    :param user_schema: 用户添加schema
    :param request:
    :return:
    """
    user = user_service.add_user(user_schema=user_schema, current_user=request.current_user)
    return R.ok(data=user)


@user_router.put("/{_id}")
@log(OperationTypeEnum.ADMIN_USER_UPDATE)
@permission_required(UserRoleEnum.ADMIN.value)
def update_by_id(*, _id: int = Path(default=0), user_schema: UserUpdateSchema, request: Request = None):
    """
    根据用户ID更新用户
    :param _id: 用户ID
    :param user_schema: 用户更新schema
    :param request:
    :return:
    """
    update_user = user_service.update_user(_id=_id, user_schema=user_schema, current_user=request.current_user)
    return R.ok(data=update_user)


@user_router.get("")
@permission_required()
def get_by_page(
        current_page: Optional[int] = 1,
        page_size: Optional[int] = 20,
        username: Optional[str] = Query(default=""),
        status: Optional[str] = Query(default=""),
        real_name: Optional[str] = Query(default=""),
        role: Optional[str] = Query(default=""),
        request: Request = None
):
    """
    用户分页查询
    :param current_page: 当前页
    :param page_size: 每页数量
    :param username: 用户名
    :param status: 用户状态
    :param real_name: 真实姓名
    :param role: 角色
    :param request:
    :return:
    """
    query_data = dict()
    if username:
        query_data.setdefault("username", username)
    if status:
        query_data.setdefault("status", status)
    if real_name:
        query_data.setdefault("real_name", real_name)
    if role:
        query_data.setdefault("role", role)

    total, users = user_service.get_users_by_page(current_page=current_page,
                                                  page_size=page_size,
                                                  username=username,
                                                  real_name=real_name,
                                                  status=status,
                                                  role=role)
    return R.ok(data=dict(total=total, list=users))


@user_router.get("/all")
def get_all():
    """
    获取所有系统内用户，用户下拉选择框
    :return:
    """
    return R.ok(data=user_service.get_users())


@user_router.post("/login")
def login(login_schema: UserLoginSchema):
    """
    用户登录
    :param login_schema: 用户名/密码
    :return:
    """
    user, token = user_service.user_login(login_schema=login_schema)
    return R.ok(data=dict(user_info=user, token=token), message="登录成功")


@user_router.delete("/many")
@permission_required(role=UserRoleEnum.ADMIN.value)
def delete_by_ids(
        request: Request = None,
        ids: str = Query(None, min_length=1)
):
    user_service.delete_user_by_ids(ids=ids, current_user=request.current_user)
    return R.ok(message="删除用户成功")


@user_router.get("/{_id}")
@permission_required()
def get_info_by_id(_id: int = Path(None), request: Request = None):
    """
    根据用户ID查询用户信息
    :param _id:
    :param request:
    :return:
    """
    user = user_service.get_user_info_by_id(_id=_id)
    return R.ok(data=user)


@user_router.delete("/{_id}")
@log(OperationTypeEnum.ADMIN_USER_DELETE.value)
@permission_required(UserRoleEnum.ADMIN.value)
def delete_by_id(_id: int = Path(default=0), request: Request = None):
    """
    根据用户ID删除用户
    :param _id: 用户ID
    :param request:
    :return:
    """
    user_service.delete_user_by_id(_id=_id, current_user=request.current_user)
    return R.ok(message="删除用户成功")
