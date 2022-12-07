from enums import BaseEnum


class StatusEnum(BaseEnum):
    """
    禁用启用状态
    """
    ENABLE = "Enable"
    DISABLE = "Disable"


class OperationTypeEnum(BaseEnum):
    """用户操作类型"""

    """用户"""
    ADMIN_USER_ADD = "管理员添加用户"
    ADMIN_USER_DELETE = "管理员删除用户"
    ADMIN_USER_UPDATE = "管理员更新用户"
    ADMIN_USER_RESET_PASSWORD = "管理员更新用户密码"
    USER_RESET_PASSWORD = "登录用户更新密码"
    USER_UPDATE = "登录用户更新信息"

    """项目"""
    PROJECT_UPDATE = "更新项目"
    PROJECT_ADD = "新建项目"
    PROJECT_DELETE = "删除项目"

    """资源"""
    RESOURCE_TYPE_ADD = "新增资源类型"
    RESOURCE_TYPE_UPDATE = "更新资源类型"
    RESOURCE_TYPE_DELETE = "删除资源类型"

    RESOURCE_ADD = "新增资源"
    RESOURCE_UPDATE = "更新资源"
    RESOURCE_DELETE = "删除资源"



class OptionTypeEnum(BaseEnum):
    OPERATION_TYPE = "operation_type"
    USER_ROLE = "user_role"
    RESOURCE_CATEGORY="resource_category"
    DATABASE_TYPE="database_type"
    PROTOCOL_TYPE="protocol_type"
    PROJECT_TYPE="project_type"
    STATUS="status"
