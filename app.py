import traceback
from typing import Union

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from pydantic import ValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
# from starlette.exceptions import ValidationError

from controller.option import option_router
from common.events import stopping, startup
from common.exception import BusinessException_400, BusinessException_401, BusinessException_404, BusinessException_403
from config.configure import settings
from controller.project import project_router
from controller.user import user_router
from controller.resource import resource_router

app = FastAPI(title=settings.SERVICE_NAME)

# 注册路由
app.include_router(project_router)
app.include_router(user_router)
app.include_router(resource_router)
app.include_router(option_router)

# 监听
app.add_event_handler("startup", startup(app))
app.add_event_handler("shutdown", stopping(app))


# 404资源不存在异常
@app.exception_handler(BusinessException_404)
def exception_404_handler(request: Request, exc: BusinessException_404):
    logger.error(f'url:{request.url},method:{request.method},headers:{request.headers}\n {exc}')
    return JSONResponse(
        status_code=exc.code,
        content={"message": f"{exc.message}"},
    )


# 用户未认证异常
@app.exception_handler(BusinessException_401)
def exception_401_handler(request: Request, exc: BusinessException_401):
    logger.error(f'url:{request.url},method:{request.method},headers:{request.headers}\n {exc}')
    return JSONResponse(
        status_code=exc.code,
        content={"message": f"{exc.message}"}
    )


# 用户未无权限异常
@app.exception_handler(BusinessException_403)
def exception_403_handler(request: Request, exc: BusinessException_403):
    logger.error(f'url:{request.url},method:{request.method},headers:{request.headers}\n {exc}')
    return JSONResponse(
        status_code=exc.code,
        content={"message": f"无访问权限，请联系管理员；{exc.message}"}
    )


# 其他业务异常
@app.exception_handler(BusinessException_400)
def exception_400_handler(request: Request, exc: BusinessException_400):
    logger.error(f'url:{request.url},method:{request.method},headers:{request.headers}\n {exc}')
    return JSONResponse(
        status_code=exc.code,
        content={"message": f"{exc.message}"}
    )


# 处理入参数据校验错误
@app.exception_handler(RequestValidationError or ValidationError)
def exception_422_handler(request: Request, exc: Union[RequestValidationError, ValidationError]):
    """
    参数校验错误处理
    :param request:
    :param exc:
    :return:
    """
    logger.error(f'url:{request.url},method:{request.method},headers:{request.headers}\n {exc}')

    errors = exc.errors()
    error = errors[0] if errors else dict()
    attr = error.get("loc") or ""
    msg = error.get("msg") or ""
    return JSONResponse(
        {
            "message": f"数据校验错误 {attr} {msg}",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


# 捕获全部异常
@app.exception_handler(Exception)
def all_exception_handler(request: Request, exc: Exception):
    """
    全局所有异常
    :param request:
    :param exc:
    :return:
    """
    logger.error(f"全局异常\n{request.method} URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    return JSONResponse(status_code=500, content={'message': f"系统异常，请联系管理员；{exc}"})


# 设置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=settings.SERVICE_PORT)
