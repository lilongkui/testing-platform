import datetime
import json
from functools import wraps

from starlette.requests import Request
from starlette.responses import JSONResponse

from common.exception import BusinessException_400
from models.user_model import UserModel


def log(operation):
    """
    写入操作日志装饰器，限制条件🚫
    1、路由函数必须带有【request】参数
    2、必须先使用【permission_required】权限验证装饰器，
      request参数setattr current_user属性用来获取当前登录用户
    :param operation:
    :return:
    """

    def wrapper(func):
        @wraps(func)
        async def sub_wrapper(*args, **kwargs):
            result: JSONResponse = func(*args, **kwargs)
            request: Request = kwargs.get("request")
            if not request:
                raise BusinessException_400("使用操作日志装饰器必须，路由函数必须带有【request】参数")

            if not hasattr(request, "current_user"):
                raise BusinessException_400("使用操作日志装饰器必须，必须先使用【permission_required】权限验证装饰器")

            #请求执行成功时，写入日志
            if result and result.status_code==200:
                user_model: UserModel = request.current_user
                from crud.crud_operation_log import operation_log
                data = dict(
                    operation=operation,
                    user_id=user_model.id,
                    username=user_model.username,
                    user_agent=request.headers.get('user-agent'),
                    method=request.method,
                    path=request.get("path"),
                    params=json.dumps(dict(request.query_params)),
                    body=bytes(await request.body()).decode(),
                    request_time=datetime.datetime.now()
                )
                operation_log.add(data)
            return result

        return sub_wrapper

    return wrapper
