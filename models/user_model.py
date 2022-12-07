from sqlalchemy import Column, String, Integer

from models import BaseDbModel


class UserModel(BaseDbModel):
    __tablename__ = 't_user'
    # 真实姓名
    real_name = Column(String(100), nullable=False)
    # 用户名
    username = Column(String(100), nullable=False, index=True)
    # 密码
    password = Column(String(100), nullable=False)
    # 角色:admin管理员，normal普通用户
    role = Column(String(100), nullable=False)
    # Enable：可用，Disable：不可用
    status = Column(String(20), nullable=False)
