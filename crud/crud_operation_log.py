from crud import BaseCRUD
from models.operation_log_model import OperationLogModel


class OperationLogCRUD(BaseCRUD):
    pass


operation_log=OperationLogCRUD(OperationLogModel)