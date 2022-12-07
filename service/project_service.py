from typing import Tuple, List

from common.exception import BusinessException_404, BusinessException_400
from crud.crud_project import project as project_crud
from models.project_model import ProjectModel
from models.user_model import UserModel
from schemas.project_schema import ProjectUpdateSchema


class ProjectService:
    def __init__(self):
        self.__project_crud = project_crud

    def add_project(self, project_schema: ProjectModel, current_user: UserModel):
        """
        新建项目
        :param project_schema:
        :param current_user:
        :return:
        """
        # 检查项目是否存在
        exits_project = self.__project_crud.get_by_condition_with_and(exact_match=True, name=project_schema.name)
        if exits_project:
            raise BusinessException_400(message=f"项目【{project_schema.name}】已经存在")
        return self.__project_crud.add(schema=project_schema, current_user=current_user)

    def update_project(self, _id: int, project_schema: ProjectUpdateSchema, current_user: UserModel):
        """
        更新项目
        :param _id:
        :param project_schema:
        :param current_user:
        :return:
        """

        # 检查项目是否存在
        exits_project: ProjectModel = self.__project_crud.get_one_by_sql_condition(
            f"name='{project_schema.name}' and id!={_id}")
        if exits_project:
            raise BusinessException_400(message=f"项目【{project_schema.name}】已经存在,ID为【{exits_project.id}】")
        return self.__project_crud.update(_id=_id, schema=project_schema, current_user=current_user)

    def get_project_by_id(self, _id):
        """
        根据project_id获取项目信息
        :param _id: 项目ID
        :return:
        """
        current_project = self.__project_crud.get_by_id(_id=_id)
        if not current_project:
            raise BusinessException_404(message=f"项目不存在：{_id}")
        return current_project

    def get_all_project(self):
        return self.__project_crud.get_by_condition_with_and()

    def get_projects_by_page(self, current_page: int,
                             page_size: int,
                             name: str,
                             type: str) -> Tuple[int, List[ProjectModel]]:
        """
        获取用户列表
        :param name:
        :param type:
        :param current_page:
        :param page_size:
        :return:
        """
        total, projects = self.__project_crud.page(current_page=current_page, page_size=page_size, name=name, type=type)
        return total, projects

    def delete_project_by_id(self, _id: int):
        # 校验项目内数据再进行删除 todo
        self.__project_crud.delete_by_id(_id=_id)


project_service = ProjectService()
