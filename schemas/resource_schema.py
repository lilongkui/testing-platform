from pydantic import Field

from enums.resource_enum import ResourceCategoryEnum, ProtocolTypeEnum, DatabaseTypeEnum
from schemas import BaseSchema


class ResourceSchema(BaseSchema):
    name: str = Field(title="名称", max_length=100, min_length=1)
    remark: str = Field(title="备注", max_length=500, default=None)


# 资源类型的添加
class ResourceTypeAddSchema(ResourceSchema):
    project_id: int = Field(title="项目ID", gt=0)
    category: ResourceCategoryEnum = Field(title="项目ID")


# 资源类型的修改
class ResourceTypeUpdateSchema(ResourceSchema):
    pass


# http类型的资源的修改
class ResourceHttpUpdateSchema(ResourceSchema):
    protocol: ProtocolTypeEnum = Field(title="协议")
    host: str = Field(title="Host/IP")
    port: int = Field(title="端口", gt=0)


# http类型的资源的添加
class ResourceHttpAddSchema(ResourceSchema):
    project_id: int = Field(title="项目ID", gt=0)
    resource_type: str = Field(title="资源类型", max_length=100, min_length=1)
    protocol: ProtocolTypeEnum = Field(title="协议")
    host: str = Field(title="Host/IP")
    port: int = Field(title="端口", gt=0)


# shell类型的资源的修改
class ResourceShellUpdateSchema(ResourceSchema):
    host: str = Field(title="资源类型", max_length=100, min_length=1)
    port: int = Field(title="端口", gt=0)
    username: str = Field(title="用户名", max_length=100)
    password: str = Field(title="密码", max_length=100)


# shell类型的资源的添加
class ResourceShellAddSchema(ResourceSchema):
    project_id: int = Field(title="项目ID", gt=0)
    resource_type: str = Field(title="资源类型", max_length=100, min_length=1)
    host: str = Field(title="资源类型", max_length=100, min_length=1)
    port: int = Field(title="端口", gt=0)
    username: str = Field(title="用户名", max_length=100)
    password: str = Field(title="密码", max_length=100)


# Database类型的资源的修改
class ResourceDatabaseUpdateSchema(ResourceSchema):
    db_type: DatabaseTypeEnum = Field(title="数据库类型")
    db_name: str = Field(title="数据库名称", max_length=100, min_length=1)
    host: str = Field(title="资源类型", max_length=100, min_length=1)
    port: int = Field(title="端口", gt=0)
    username: str = Field(title="用户名", max_length=100)
    password: str = Field(title="密码", max_length=100)
    charset: str = Field(title="密码", max_length=100, default=None)


# Database类型的资源的添加
class ResourceDatabaseAddSchema(ResourceSchema):
    project_id: int = Field(title="项目ID", gt=0)
    resource_type: str = Field(title="资源类型", max_length=100, min_length=1)
    db_type: DatabaseTypeEnum = Field(title="数据库类型")
    db_name: str = Field(title="数据库名称", max_length=100, min_length=1)
    host: str = Field(title="资源类型", max_length=100, min_length=1)
    port: int = Field(title="端口", gt=0)
    username: str = Field(title="用户名", max_length=100)
    password: str = Field(title="密码", max_length=100)
    charset: str = Field(title="密码", max_length=100, default=None)
