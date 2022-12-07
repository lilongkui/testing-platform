from pydantic import Field, EmailStr

from enums.common_enum import StatusEnum
from enums.user_enum import UserRoleEnum
from schemas import BaseSchema


class UserSchema(BaseSchema):
    username: EmailStr = Field(description="账号必须是邮箱格式", title="账号")
    real_name: str = Field(min_length=1, max_length=100, description="真实姓名1～100个字符", title="真实姓名")
    role: UserRoleEnum = Field(title="用户角色")
    status: StatusEnum = Field(default=StatusEnum.ENABLE.value, title="是否激活")


class UserLoginSchema(BaseSchema):
    username: EmailStr = Field(title="账号")
    password: str = Field(min_length=8, max_length=100, title="密码")


class UserAddSchema(UserSchema):
    password: str = Field(min_length=8, max_length=100, title="密码")


class UserResetPasswordSchema(BaseSchema):
    old_password: str = Field(min_length=8, max_length=100, title="原始密码")
    new_password: str = Field(min_length=8, max_length=100, title="新密码")
    confirm_new_password: str = Field(min_length=8, max_length=100, title="确认密码")


class UserUpdateSchema(BaseSchema):
    real_name: str = Field(min_length=1, max_length=10, title="真实姓名")
    role: UserRoleEnum = Field(title="用户角色")
    status: str = Field(None)
