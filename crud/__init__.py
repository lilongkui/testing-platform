from typing import Tuple, List, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_, text, desc

from db.mysql import SessionFactory
from models.user_model import UserModel


class BaseCRUD:
    def __init__(self, model):
        self.model = model

    def add(self, schema, current_user: UserModel = None) -> Any:
        """
        根据schema对象转成model对象，存入数据库
        :param current_user: 用户对象
        :param schema: 继承了BaseModel的schema对象
        :return:
        """
        # 将Pedantic的对象转换成json对象
        data = jsonable_encoder(schema)
        model = self.model(**data)
        if hasattr(self.model, "creator_id") and current_user:
            model.creator_id = current_user.id
        if hasattr(self.model, "updater_id") and current_user:
            model.updater_id = current_user.id
        with SessionFactory() as session:
            session.add(model)
            session.commit()
            session.refresh(model)
        return model

    def update(self, _id, schema, current_user: UserModel = None) -> Any:
        """
        根据id更新数据
        :param _id: id号
        :param schema: 待更新的数据
        :param current_user: 用户对象
        :return: 更新后的数据
        """
        # 根据id号从数据库读取需要更新的数据
        with SessionFactory() as session:
            db_obj = session.query(self.model).get(_id)
            if not db_obj:
                return db_obj
            obj_data = jsonable_encoder(db_obj)
            update_data = schema if isinstance(schema, dict) else jsonable_encoder(schema)
            [setattr(db_obj, field, update_data.get(field)) for field in obj_data if field in update_data]
            if hasattr(self.model, "updater_id") and current_user:
                setattr(db_obj, "updater_id", current_user.id)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj

    def delete_by_id(self, _id) -> Any:
        """
        根据id删除数据
        :param _id: id号
        :return:
        """
        with SessionFactory() as session:
            db_obj = session.query(self.model).get(_id)
            if not db_obj:
                return db_obj
            session.delete(db_obj)
            session.commit()
            return db_obj

    def get_one_by_sql_condition(self, condition: str) -> Any:
        """
        使用标准的sql查询条件查询一条符合条件的记录
        :param condition: eg.id=1
        :return:
        """
        with SessionFactory() as session:
            return session.query(self.model).filter(text(condition)).first()

    def get_all_by_sql_condition(self, condition: str) -> List[Any]:
        """
        使用标准的sql查询条件查询所有符合条件的记录
        :param condition: eg.id=1
        :return:
        """
        with SessionFactory() as session:
            return session.query(self.model).filter(text(condition)).order_by(desc(self.model.id)).all()

    def get_by_id(self, _id) -> Any:
        """
        根据model的id获取model对象
        :param _id: model的ID
        :return:
        """
        with SessionFactory() as session:
            return session.query(self.model).get(_id)

    def __get_condition(self, exact_match=False, **kwargs):
        """
        组装查询条件，仅内部使用
        :param exact_match:是否精准匹配，默认为False，模糊匹配
        :param kwargs:
        :return:
        """
        if exact_match:
            list_condition = [f"self.model.{k}=='{v}'" for k, v in kwargs.items() if v is not None and v != ""]
        else:
            list_condition = [f"self.model.{k}.like('%{v}%')" for k, v in kwargs.items() if v is not None and v != ""]
        conditions = []
        for item in list_condition:
            conditions.append(eval(item))
        return conditions

    def get_by_condition_with_and(self, exact_match=False, **kwargs) -> List[Any]:
        """
        根据字典格式的条件进行查询，条件之间的关系为And
        :param exact_match: 是否为精准匹配，默认为模糊查询
        :param kwargs:查询条件
        :return:
        """
        conditions = self.__get_condition(exact_match, **kwargs)
        with SessionFactory() as session:
            return session.query(self.model).filter(and_(*conditions)).order_by(desc(self.model.id)).all()

    def get_by_condition_with_or(self, exact_match=False, **kwargs) -> List[Any]:
        """
        根据字典格式的条件进行查询，条件之间的关系为Or
        :param exact_match: 是否为精准匹配，默认为模糊查询
        :param kwargs:查询条件
        :return:
        """
        conditions = self.__get_condition(exact_match, **kwargs)
        with SessionFactory() as session:
            return session.query(self.model).filter(or_(text(*conditions))).order_by(desc(self.model.id)).all()

    def page(self, current_page: int = 1, page_size: int = 20, order="asc", **kwargs) -> Tuple[int, list]:
        """
        可选条件的分页查询
        :param order: 排序
        :param current_page: 起始位置
        :param page_size: 数据条数
        :param kwargs: 查询条件
        :return:
        """
        list_condition = [f"self.model.{k}.like('%{v}%')" for k, v in kwargs.items() if v is not None and v != ""]
        conditions = []
        for item in list_condition:
            conditions.append(eval(item))
        with SessionFactory() as session:
            if order == "desc":
                all_data = session.query(self.model).filter(and_(*conditions)).order_by(desc(self.model.id)).all()
            else:
                all_data = session.query(self.model).filter(and_(*conditions)).all()
            total = len(all_data)
            return total, all_data[(current_page - 1) * page_size: current_page * page_size]

    def delete_by_ids(self, ids: List[int]) -> None:
        """
        根据模型id列表删除
        :param ids:id列表
        :return:
        """
        with SessionFactory() as session:
            session.query(self.model).filter(self.model.id.in_(ids)).delete()
            session.commit()
