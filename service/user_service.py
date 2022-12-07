from typing import Tuple, List

from common.exception import BusinessException_400, BusinessException_404
from common.utils import en_password, check_password, generate_token, id_str2int_list
from crud.crud_user import user as user_curd
from models.user_model import UserModel
from schemas.user_schema import UserAddSchema, UserUpdateSchema, UserLoginSchema


class UserService:
    def __init__(self):
        self.__user_crud = user_curd

    def add_user(self, user_schema: UserAddSchema, current_user: UserModel) -> UserModel:
        """
        创建用户
        :param user_schema:
        :param current_user:
        :return:
        """
        # 检查用户名是否存在
        exits_user = self.__user_crud.get_by_condition_with_and(exact_match=True, username=user_schema.username)
        if exits_user:
            raise BusinessException_400(message=f"用户[{user_schema.username}]已存在")
        user_schema.password = en_password(user_schema.password)
        return self.__user_crud.add(schema=user_schema, current_user=current_user)

    def update_user(self, _id, user_schema: UserUpdateSchema, current_user: UserModel) -> UserModel:
        """
        更新用户
        :param _id:
        :param user_schema:
        :param current_user:
        :return:
        """
        update_user = self.__user_crud.update(_id=_id, schema=user_schema, current_user=current_user)
        if not update_user:
            raise BusinessException_404(message=f"未找到用户信息，用户ID【{_id}】")
        return update_user

    def delete_user_by_id(self, _id: int, current_user: UserModel) -> UserModel:
        """
        根据用户ID删除用户
        :param current_user:
        :param _id:
        :return:
        """
        if _id == 1:
            raise BusinessException_400(message=f"不可以删除管理员【{current_user.real_name}】")
        if current_user.id == _id:
            raise BusinessException_400(message=f"不可以删除自己【{current_user.real_name}】")
        user = self.__user_crud.delete_by_id(_id=_id)
        if not user:
            raise BusinessException_400(message=f"用户ID：[{_id}]不存在")
        return user

    def get_users_by_page(self, current_page: int, page_size: int, username: str, real_name: str, status: str,
                          role: str) -> Tuple[int, List[UserModel]]:
        """
        获取用户列表
        :param role:
        :param status:
        :param real_name:
        :param username:
        :param current_page:
        :param page_size:
        :return:
        """
        total, users = self.__user_crud.page(current_page=current_page,
                                             page_size=page_size,
                                             username=username,
                                             real_name=real_name,
                                             status=status,
                                             role=role)
        return total, users

    def user_login(self, login_schema: UserLoginSchema):
        """
        用户登录
        :param login_schema: 用户名/密码
        :return:
        """
        username = login_schema.username
        origin_password = login_schema.password
        # 根据username查询用户
        user: UserModel = self.__user_crud.get_one_by_sql_condition(condition=f"username='{username}'")
        if not user or not user.status or not check_password(origin_password=origin_password,
                                                             encode_password=user.password):
            raise BusinessException_400(message=f"登录用户【{username}】不存在,或密码错误,或已被禁用")
        token = generate_token(user_id=user.id)
        return user, token

    def get_users(self):
        """
        获取系统内所有用户
        :return:
        """
        return self.__user_crud.get_by_condition_with_and()

    def get_user_info_by_id(self, _id: int):
        user = self.__user_crud.get_by_id(_id=_id)
        if not user:
            raise BusinessException_404(message=f"根据用户ID【{_id}】未查询到用户信息")
        return user

    def delete_user_by_ids(self, ids: str, current_user: UserModel):
        """
        根据ids删除user
        :param current_user:
        :param ids:
        :return:
        """
        if not ids:
            return
        ids_list = id_str2int_list(ids)
        if current_user.id in ids_list:
            raise BusinessException_400(message=f"不可以删除自己【{current_user.real_name}】")
        if 1 in ids_list:
            raise BusinessException_400(message=f"不可以删除管理员【{current_user.real_name}】")
        self.__user_crud.delete_by_ids(ids_list)


user_service = UserService()
