from sqlalchemy import String, Column

from models import BaseDbModel


class ProjectModel(BaseDbModel):
    __tablename__ = 't_project'
    name = Column(String(100), nullable=False, index=True)
    type = Column(String(20), nullable=False)
    remark = Column(String(500), nullable=True)
