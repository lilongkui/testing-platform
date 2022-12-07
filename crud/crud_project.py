from crud import BaseCRUD
from models.project_model import ProjectModel


class ProjectCRUD(BaseCRUD):
    pass


project=ProjectCRUD(ProjectModel)