# 根据数据库连接字符串创建一个数据库访问引擎对象--连接对象
# 创建会话session对象--对数据库的操作对象
# 动态创建数据库映射基类
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, session

from config.configure import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL,
                       pool_pre_ping=True)
# 创建Session对象的代码：session = SessionLocal()
SessionFactory: session = sessionmaker(autocommit=False,
                                       expire_on_commit=False,
                                       bind=engine)
# 动态创建数据库model的基类，数据库model只需要继承该类，
# 即可完成model到数据库表之间的映射
Base = declarative_base()

# 创建对象：session = SessionFactory()
# session = 对象名()，默认会执行 该对象所属的类的__call__方法
