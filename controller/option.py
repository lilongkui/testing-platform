from fastapi import APIRouter, Query
from starlette.requests import Request

from common.auth import permission_required
from common.r import R
from config.configure import settings
from service.option_service import OptionService

option_router = APIRouter(prefix=settings.PATH_PREFIX + "/options")


@option_router.get("")
@permission_required()
def get_options_by_type(option_type: str = Query(None), request: Request = None):
    """
    获取各种下拉选项的列表
    :param option_type:
    :param request:
    :return:
    """
    options = OptionService.get_options_by_type(option_type=option_type)

    return R.ok(data=options)
