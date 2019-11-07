import json

from sqlalchemy import or_

from apis.base.base_dao import BaseDao
from apis.project.models import Project
from common.helper import Serializer
from common.redis_api import redis_cli


class ProjectDao(BaseDao):

    def __init__(self):
        self.project = Project
        super(ProjectDao, self).__init__(self.project)
        self.redis_cli = redis_cli
        self.redis_prefix = "project:{}"

    def update(self, project_id, **kwargs):
        """
        更新项目
        :param project_id:
        :param kwargs:
        :return:
        """
        key = self.redis_prefix.format(str(project_id))
        self.redis_cli.delete(key)
        self.update_(project_id, **kwargs)

    def delete(self, project_id):
        """
        删除项目
        :param project_id:
        :return:
        """
        key = self.redis_prefix.format(str(project_id))
        self.redis_cli.delete(key)
        self.delete_(project_id)

    def get(self, project_id):
        """
        获取项目详情
        :param project_id:
        :return:
        """
        key = self.redis_prefix.format(str(project_id))
        project = self.redis_cli.get(key)
        if project:
            return json.loads(project) if not isinstance(project, dict) else project
        project = self.get_serializer_(project_id)
        self.redis_cli.set(key, json.dumps(project))
        return project

    def get_by_ids(self, ids, name_or_code=None, page_num=1, page_size=10):
        """
        根据多个项目id查询
        :return:
        """
        query = self.project.query.filter(self.project.id.in_(ids))
        if name_or_code:
            query = query.filter(or_(self.project.name.contains(name_or_code), self.project.code.contains(name_or_code)))
        total = query.count()
        start, end = (page_num - 1) * page_size, page_num * page_size
        data = Serializer.as_dict(query[start:end])
        return total, data

    def get_by_code(self, code):
        """
        根据项目code查询项目
        :param code:
        :return:
        """
        return self.project.query.filter_by(code=code).first()


project_dao = ProjectDao()
