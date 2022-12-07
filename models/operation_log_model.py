from sqlalchemy import Column, Integer, String, DateTime, text

from db.mysql import Base


class OperationLogModel(Base):
    __tablename__ = "h_operation_log"
    id = Column(Integer, primary_key=True, autoincrement='auto')
    operation = Column(String(100), nullable=False)
    user_id = Column(Integer, index=True)
    username = Column(String(100))
    user_agent = Column(String(200), index=True)
    method = Column(String(10), nullable=False)
    path = Column(String(200), nullable=False)
    params = Column(String(1000), nullable=False)
    body = Column(String(1000), nullable=False)
    request_time = Column(DateTime, nullable=True, server_default=text('current_timestamp'))