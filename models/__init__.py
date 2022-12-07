from sqlalchemy import Column, DateTime, text, Integer

from db.mysql import Base


class BaseDbModel(Base):
    id = Column(Integer, primary_key=True, autoincrement='auto')
    creator_id = Column(Integer, index=True)
    create_time = Column(DateTime, nullable=True, server_default=text('current_timestamp'))
    updater_id = Column(Integer, index=True)
    update_time = Column(DateTime, nullable=True, server_default=text('current_timestamp'),
                         onupdate=text('current_timestamp'))
    __abstract__ = True  # 只作为基类，被继承，不会生成表
