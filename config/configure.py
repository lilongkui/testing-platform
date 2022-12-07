import os

from common.singleton import Singleton


# 继承Singleton，实现单例模式
class Configure(Singleton):
    __initFlag = False
    __config_ini_file = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"

    def __init__(self):
        if Configure.__initFlag:
            return
        from configparser import ConfigParser
        config = ConfigParser()
        config.read(Configure.__config_ini_file)
        self.__mysql_host = config.get("mysql", "host")
        self.__mysql_port = config.getint("mysql", "port")
        self.__mysql_username = config.get("mysql", "username")
        self.__mysql_password = config.get("mysql", "password")
        self.__mysql_db = config.get("mysql", "db")

        self.__redis_host = config.get("redis", "host")
        self.__redis_port = config.getint("redis", "port")
        self.__redis_username = config.get("redis", "username")
        self.__redis_password = config.get("redis", "password")
        self.__redis_db = config.get("redis", "db")

        self.__service_name = config.get("service", "name")
        self.__service_port = config.getint("service", "port")

        self.__secret_key = config.get("token", "secret_key")
        self.__expire = config.getint("token", "expire")
        self.__path_prefix=config.get("service", "path_prefix")
        Configure.__initFlag = True

    @property
    def MYSQL_HOST(self):
        return self.__mysql_host

    @property
    def MYSQL_PORT(self):
        return self.__mysql_port

    @property
    def MYSQL_USERNAME(self):
        return self.__mysql_username

    @property
    def MYSQL_PASSWORD(self):
        return self.__mysql_password

    @property
    def MYSQL_DB(self):
        return self.__mysql_db

    @property
    def SERVICE_NAME(self):
        return self.__service_name

    @property
    def SERVICE_PORT(self):
        return self.__service_port

    @property
    def SQLALCHEMY_DATABASE_URL(self):
        return f"mysql+pymysql://{self.MYSQL_USERNAME}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    @property
    def REDIS_HOST(self):
        return self.__redis_host

    @property
    def REDIS_PORT(self):
        return self.__redis_port

    @property
    def REDIS_USERNAME(self):
        return self.__redis_username

    @property
    def REDIS_PASSWORD(self):
        return self.__redis_password

    @property
    def REDIS_DB(self):
        return self.__redis_db

    @property
    def TOKEN_SECRET_KEY(self):
        return self.__secret_key

    @property
    def TOKEN_EXPIRE(self):
        return self.__expire

    @property
    def PATH_PREFIX(self):
        return self.__path_prefix


settings = Configure()
