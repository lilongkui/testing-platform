from datetime import datetime
from typing import List

from pydantic import Field

from enums.project_enum import ProjectTypeEnum
from schemas import BaseResponseSchema, BaseResponsePageSchema, BaseSchema


class ProjectSchema(BaseSchema):
    name: str = Field(min_length=2, max_length=100, description="项目名称")
    type: ProjectTypeEnum = Field()
    remark: str = Field(max_length=500, description="项目描述", default=None)


class ProjectUpdateSchema(ProjectSchema):
    pass


class ProjectAddSchema(ProjectSchema):
    pass


class ProjectSelectionSchema(ProjectSchema):
    creator_id: int = None
    create_time: datetime = None
    updater_id: int = None
    update_time: datetime = None


class ProjectResponseSchema(BaseResponseSchema):
    data: ProjectSelectionSchema


class ProjectResponsePageSchema(BaseResponsePageSchema):
    data: List[ProjectSelectionSchema]
    total: int


class ProjectResponseListSchema(BaseResponsePageSchema):
    data: List[ProjectSelectionSchema]
