from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


class R:
    @staticmethod
    def ok(message='success', data=None):
        data = jsonable_encoder(data)
        return JSONResponse(status_code=200,
                            content={
                                'code': 200,
                                'message': message,
                                'data': data}
                            )

    @staticmethod
    def error(message='操作失败', data=None):
        data = jsonable_encoder(data)
        return JSONResponse(status_code=400,
                            content={
                                'code': 400,
                                'message': message,
                                'data': data}
                            )
