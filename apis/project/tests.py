import unittest

from apis.application.dao import config_dao
from apis.project.functions import ProjectTool
from apis.project.dao import project_dao
from app import app


class ProjectTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config[
            'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:cmdt1234@10.176.139.10:3306/devops2.0?charset=utf8mb4"
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.project_tool = ProjectTool

    def test_list_project(self):
        dao = project_dao
        res = dao.update(3, name="hhhhhh")
        print(res)

    def test_search(self):
        dao = project_dao
        res = dao.search_()
        print(res)

    def test_delete(self):
        res = config_dao.get_by_app_id_bak(1)
        result = {}
        for _res in res:
            if _res['id'] in result:
                result[_res['id']]['data'].append(_res)
            else:
                result[_res['id']] = {'id': _res['id'], 'version': _res['version'], 'app_id': _res['app_id'],
                                      'data': [_res]}
        print(res)
        print(result)
        print(result.values())

    def test_project_statistics(self):
        tool = self.project_tool()
        res = tool.statistics([76, 77, 78, 79, 80, 146, 147, 149])
        print(res)

    def tearDown(self) -> None:
        self.app_ctx.pop()
