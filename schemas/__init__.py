from typing import List

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class config:
        orm_mode = True


class BaseResponseSchema(BaseSchema):
    code: int = 200
    message: str = 'success'
    data: dict = {}


class BaseResponsePageSchema(BaseSchema):
    code: int = 200
    message: str = 'success'
    data: List = list()
    total: int = 0
