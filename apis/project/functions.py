import re
from apis.project.dao import project_dao
from common.exceptions import InputError
from common.execute_sql import dict_fetchall
from common.message import msg_const
from common.redis_api import redis_cli


class ProjectTool(object):
    def __init__(self):
        self.redis_cli = redis_cli
        self.project_dao = project_dao
        self.dict_fetchall = dict_fetchall

    def valid_project_code(self, code):
        """
        对项目的code值进行校验
        :param code:
        :return:
        """
        res = re.match('[a-z][a-z0-9]{2,10}$', code)
        if not res:
            return {"available": False, "message": "项目参数code格式有误"}
        counter = self.project_dao.total_(code=code)
        if counter != 0:
            return {"available": False, "message": "项目参数code已存在"}
        return {"available": True, "message": "ok"}

    def valid_params(self, **kwargs):
        if 'name' not in kwargs:
            raise InputError(msg_const.PROJECT_NAME_404)
        if 'owner' not in kwargs:
            raise InputError(msg_const.PROJECT_OWNER_404)
        if kwargs['owner'] == 0:
            raise InputError(msg_const.PROJECT_OWNER_403)
        if 'code' not in kwargs:
            raise InputError(msg_const.PROJECT_CODE_404)
        self.valid_project_code(kwargs.get('code'))

    def statistics(self, project_ids):
        """
        获取项目对应的应用数量、环境数量、成员数量、流水线数量
        :return:
        """
        app_sql = """select project_id, count(1) as app_total from application where project_id in :project_ids group 
        by project_id"""
        app_info = self.dict_fetchall(app_sql, {'project_ids': project_ids})
        app_info = {app['project_id']: app['app_total'] for app in app_info}
        env_sql = """select project_id, count(1) as env_total from environment where project_id in :project_ids group 
        by project_id"""
        env_info = self.dict_fetchall(env_sql, {'project_ids': project_ids})
        env_info = {env['project_id']: env['env_total'] for env in env_info}
        running_pipeline_sql = """select project_id, count(1) as pipeline_total from pipeline where project_id 
                in :project_ids and status='running' group by project_id"""
        running_pipeline_info = self.dict_fetchall(running_pipeline_sql, {'project_ids': project_ids})
        running_pipeline_info = {running_pipeline['project_id']: running_pipeline['pipeline_total'] for
                                 running_pipeline in running_pipeline_info}
        pipeline_sql = """select project_id, count(1) as pipeline_total from pipeline where project_id in :project_ids 
        group by project_id"""
        pipeline_info = self.dict_fetchall(pipeline_sql, {'project_ids': project_ids})
        pipeline_info = {
            pipeline['project_id']: str(running_pipeline_info.get(pipeline['project_id'], 0)) + '/' + str(
                pipeline['pipeline_total'])
            for pipeline in pipeline_info}
        return {_id: {'appCnt': app_info.get(_id, 0), 'envCnt': env_info.get(_id, 0),
                      'pipelineCnt': pipeline_info.get(_id, '0/0'), 'memberCnt': 0} for _id in project_ids}

    def get_user_infos(self, user_ids):
        """
        根据user_ids批量获取用户信息
        :param user_ids:
        :return:
        """
        users = self.user_dao.get_user_info_by_ids(user_ids)
        return {user.get('id'): {'ownerName': user.get('username'), 'ownerEmail': user.get('email')} for user in users}
