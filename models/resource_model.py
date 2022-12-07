from sqlalchemy import Column, String, Integer

from models import BaseDbModel


class ResourceTypeModel(BaseDbModel):
    __tablename__ = "t_resource_type"
    project_id = Column(Integer, nullable=False, index=True, comment='项目ID')
    category = Column(String(100), nullable=False, comment='资源分类，http、database、shell等')
    name = Column(String(100), nullable=False, comment='资源名称')
    remark = Column(String(500), comment='备注')

class ResourceHttpModel(BaseDbModel):
    __tablename__ = "t_resource_http"
    # 项目名称
    project_id = Column(Integer, nullable=False, index=True, comment='项目ID')
    name = Column(String(100), nullable=False, comment='资源名称')
    resource_type = Column(String(100), nullable=False, comment='资源类型')
    protocol = Column(String(100), nullable=False, comment='协议：http，https')
    host = Column(String(100), nullable=False, comment='Host/IP')
    port = Column(Integer, nullable=False, comment='端口')
    remark = Column(String(500), comment='备注')


class ResourceShellModel(BaseDbModel):
    __tablename__ = "t_resource_shell"
    project_id = Column(Integer, nullable=False, index=True, comment='项目ID')
    name = Column(String(100), nullable=False, comment='资源名称')
    resource_type = Column(String(100), nullable=False, comment='资源类型')
    host = Column(String(20), nullable=False, comment='Host/IP')
    port = Column(Integer, nullable=False, comment='端口')
    username = Column(String(100), nullable=False, comment='用户名')
    password = Column(String(100), nullable=False, comment='密码')
    remark = Column(String(500), comment='备注')


class ResourceDatabaseModel(BaseDbModel):
    __tablename__ = "t_resource_database"
    project_id = Column(Integer, nullable=False, index=True, comment='项目ID')
    name = Column(String(100), nullable=False, comment='资源名称')
    resource_type = Column(String(100), nullable=False, comment='资源类型')
    db_type = Column(String(100), nullable=False, comment='db类型mysql等')
    db_name = Column(String(100), nullable=False, comment='数据库名称')
    host = Column(String(20), nullable=False, comment='Host/IP')
    port = Column(Integer, nullable=False, comment='端口')
    username = Column(String(100), nullable=False, comment='用户名')
    password = Column(String(100), nullable=False, comment='密码')
    charset = Column(String(100), comment='字符集')
    remark = Column(String(500), comment='备注')
