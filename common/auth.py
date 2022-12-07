from functools import wraps

from common.exception import BusinessException_401, BusinessException_403, BusinessException_400
from common.utils import verification_token
from crud.crud_user import user as user_crud
from enums.common_enum import StatusEnum
from enums.user_enum import UserRoleEnum
from models.user_model import UserModel


def permission_required(role=UserRoleEnum.NORMAL.value):
    def wrapper(func):
        @wraps(func)
        def sub_wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if not request:
                raise BusinessException_400("使用权限验证装饰器必须，路由函数必须带有【request】参数")
            headers = request.headers
            token = headers.get("token")
            if not token:
                raise BusinessException_401(message="请重新登录")
            user_id = verification_token(token)
            user_model: UserModel = user_crud.get_by_id(_id=user_id)
            if not user_model:
                raise BusinessException_401(message="用户信息不存在")
            if user_model.status == StatusEnum.DISABLE.value:
                raise BusinessException_401(message="用户已被禁用")
            # 需要Root权限
            if role == UserRoleEnum.ROOT.value and user_model.role != UserRoleEnum.ROOT.value:
                raise BusinessException_403(message=f"用户无权限访问，需要{UserRoleEnum.ADMIN.value}权限")
            # 需要Admin权限
            if role == UserRoleEnum.ADMIN.value and user_model.role not in (
                    UserRoleEnum.ADMIN.value, UserRoleEnum.ROOT.value):
                raise BusinessException_403(message=f"用户无权限访问，需要{UserRoleEnum.ADMIN.value}权限")
            setattr(request, "current_user", user_model)
            return func(*args, **kwargs)

        return sub_wrapper

    return wrapper
