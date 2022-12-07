from enums.common_enum import StatusEnum, OptionTypeEnum, OperationTypeEnum
from enums.project_enum import ProjectTypeEnum
from enums.user_enum import UserRoleEnum
from enums.resource_enum import ResourceCategoryEnum, DatabaseTypeEnum, ProtocolTypeEnum


class OptionService(object):
    def __init__(self):
        pass
    @staticmethod
    def get_options_by_type(option_type: str):
        """
        根据不同下拉选项类型获取下拉选项
        :param option_type:
        :return:
        """
        options = list()
        if option_type == OptionTypeEnum.OPERATION_TYPE.value:
            options = OperationTypeEnum.values()
        elif option_type == OptionTypeEnum.DATABASE_TYPE.value:
            options = DatabaseTypeEnum.values()
        elif option_type == OptionTypeEnum.PROJECT_TYPE.value:
            options = ProjectTypeEnum.values()
        elif option_type == OptionTypeEnum.STATUS.value:
            options = StatusEnum.values()
        elif option_type == OptionTypeEnum.USER_ROLE.value:
            options = UserRoleEnum.values()
        elif option_type == OptionTypeEnum.RESOURCE_CATEGORY.value:
            options = ResourceCategoryEnum.values()
        elif option_type == OptionTypeEnum.PROTOCOL_TYPE.value:
            options = ProtocolTypeEnum.values()
        return options
