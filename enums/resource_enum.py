from enums import BaseEnum


class ResourceCategoryEnum(BaseEnum):
    HTTP = "Http"
    SHELL = "Shell"
    DATABASE = "Database"


class DatabaseTypeEnum(BaseEnum):
    MYSQL = "Mysql"
    ORACLE = "Oracle"


class ProtocolTypeEnum(BaseEnum):
    HTTP = "Http"
    HTTPS = "Https"