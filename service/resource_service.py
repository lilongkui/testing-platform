from typing import List, Tuple

from enums.resource_enum import ResourceCategoryEnum
from common.exception import BusinessException_404, BusinessException_400
from crud.crud_resource import ResourceCRUD
from models.resource_model import ResourceTypeModel, ResourceHttpModel, ResourceShellModel, ResourceDatabaseModel
from models.user_model import UserModel
from schemas.resource_schema import ResourceTypeAddSchema, ResourceTypeUpdateSchema
from schemas.resource_schema import ResourceHttpAddSchema, ResourceHttpUpdateSchema
from schemas.resource_schema import ResourceShellAddSchema, ResourceShellUpdateSchema
from schemas.resource_schema import ResourceDatabaseAddSchema, ResourceDatabaseUpdateSchema


class ResourceService:
    def __init__(self):
        self.__resource_type_crud = ResourceCRUD(ResourceTypeModel)
        self.__resource_crud_map = {
            ResourceCategoryEnum.HTTP.value: ResourceCRUD(ResourceHttpModel),
            ResourceCategoryEnum.SHELL.value: ResourceCRUD(ResourceShellModel),
            ResourceCategoryEnum.DATABASE.value: ResourceCRUD(ResourceDatabaseModel)
        }

    # ------资源类型的处理方法start------------

    def add_resource_type(self, schema: ResourceTypeAddSchema, current_user: UserModel):
        # 转大写
        schema.name = schema.name.upper()
        # 检查重名
        exits_resource_type: List[ResourceTypeModel] = self.__resource_type_crud.get_by_condition_with_and(
            exact_match=True,
            name=schema.name,
            project_id=schema.project_id,
            category=schema.category)
        if exits_resource_type:
            raise BusinessException_400(message=f"资源类型已经存在【{schema.name}】")
        return self.__resource_type_crud.add(schema=schema, current_user=current_user)

    def update_resource_type_by_id(self, _id: int, schema: ResourceTypeUpdateSchema, current_user: UserModel):
        # 检查当前更新的数据是否存在
        current_resource_type = self.__resource_type_crud.get_by_id(_id=_id)
        if not current_resource_type:
            raise BusinessException_404(message=f"资源类型不存在ID：【{_id}】")
        # 检查重名
        exits_resource_type: List[ResourceTypeModel] = self.__resource_type_crud.get_by_condition_with_and(
            exact_match=True,
            name=schema.name,
            project_id=current_resource_type.project_id,
            category=current_resource_type.category
        )
        if exits_resource_type and exits_resource_type[0].id != _id:
            raise BusinessException_400(message=f"资源类型已经存在【{schema.name}】")
        return self.__resource_type_crud.update(_id=_id, schema=schema, current_user=current_user)

    def delete_resource_type_by_id(self, _id):
        current_resource_type = self.__resource_type_crud.delete_by_id(_id=_id)
        if not current_resource_type:
            raise BusinessException_404(message=f"资源类型不存在ID：【{_id}】")
        return current_resource_type

    def get_all_resource_type(self, project_id, category):
        resource_type_list = self.__resource_type_crud.get_by_condition_with_and(
            exact_match=True,
            project_id=project_id,
            category=category)
        return resource_type_list

    # ------资源类型的处理方法end------------

    # ------资源的处理方法start------------
    def add_resource(self,
                     http: ResourceHttpAddSchema,
                     shell: ResourceShellAddSchema,
                     database: ResourceDatabaseAddSchema,
                     category: ResourceCategoryEnum,
                     current_user: UserModel):
        """
        新增资源
        :param http:
        :param shell:
        :param database:
        :param category:
        :param current_user:
        :return:
        """
        if category == ResourceCategoryEnum.HTTP.value:
            resource_schema = http
        elif category == ResourceCategoryEnum.SHELL.value:
            resource_schema = shell
        elif category == ResourceCategoryEnum.DATABASE.value:
            resource_schema = database
        else:
            raise BusinessException_400(message=f"资源分类错误【{category}】")
        resource_crud = self.__resource_crud_map.get(category)
        exits_resource = resource_crud.get_by_condition_with_and(
            exact_match=True,
            project_id=resource_schema.project_id,
            name=resource_schema.name
        )
        if exits_resource:
            raise BusinessException_400(message=f"资源【{resource_schema.name}】已经存在")
        return resource_crud.add(schema=resource_schema, current_user=current_user)

    def update_resource(self,
                        _id,
                        http: ResourceHttpUpdateSchema,
                        shell: ResourceShellUpdateSchema,
                        database: ResourceDatabaseUpdateSchema,
                        category: ResourceCategoryEnum,
                        current_user: UserModel):
        """
        新增资源
        :param _id: 资源ID
        :param http:
        :param shell:
        :param database:
        :param category:
        :param current_user:
        :return:
        """
        if category == ResourceCategoryEnum.HTTP.value:
            resource_schema = http
        elif category == ResourceCategoryEnum.SHELL.value:
            resource_schema = shell
        elif category == ResourceCategoryEnum.DATABASE.value:
            resource_schema = database
        else:
            raise BusinessException_400(message=f"资源分类错误【{category}】")

        resource_crud = self.__resource_crud_map.get(category)
        current_resource = resource_crud.get_by_id(_id=_id)
        if not current_resource:
            raise BusinessException_404(message=f"ID:【{_id}】的资源不存在")
        # 检查重名
        exits_resource = resource_crud.get_by_condition_with_and(
            exact_match=True,
            project_id=current_resource.project_id,
            name=resource_schema.name
        )
        if exits_resource and exits_resource[0].id != _id:
            raise BusinessException_400(message=f"资源【{resource_schema.name}】已经存在")
        return resource_crud.update(_id=_id, schema=resource_schema, current_user=current_user)

    def delete_resource(self, _id, category):
        """
        根据id删除资源
        :param _id:
        :param category:
        :return:
        """
        resource_crud = self.__resource_crud_map.get(category)
        resource_crud.delete_by_id(_id=_id)

    def get_resources_by_page(self, current_page, page_size, name, project_id, category) -> Tuple[int, List]:
        resource_crud = self.__resource_crud_map.get(category)
        total, resources = resource_crud.page(current_page=current_page,
                                              page_size=page_size,
                                              name=name,
                                              project_id=project_id,
                                              order="desc")
        return total, resources

    def get_all_resource_by_category(self, project_id):
        result = dict()
        http_resource_crud = self.__resource_crud_map.get(ResourceCategoryEnum.HTTP.value)
        shell_resource_crud = self.__resource_crud_map.get(ResourceCategoryEnum.SHELL.value)
        database_resource_crud = self.__resource_crud_map.get(ResourceCategoryEnum.DATABASE.value)
        https = http_resource_crud.get_all_by_sql_condition(f"project_id={project_id}")
        shells = shell_resource_crud.get_all_by_sql_condition(f"project_id={project_id}")
        databases = database_resource_crud.get_all_by_sql_condition(f"project_id={project_id}")
        result.update({"http": https, "shell": shells, "database": databases})
        return result
    # ------资源的处理方法end------------


resource_service = ResourceService()
