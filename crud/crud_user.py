from crud import BaseCRUD
from models.user_model import UserModel


class UserCRUD(BaseCRUD):pass
user=UserCRUD(UserModel)