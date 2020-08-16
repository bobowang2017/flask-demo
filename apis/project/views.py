import time

from flask import request
from flask_restful import Resource
from common.helper import standard_resp, result_to_camel_case, rate_limit
from exts import logger
import os


class ProjectListResource(Resource):
    @standard_resp
    @result_to_camel_case
    def get(self):
        """
        查询项目列表
        ---
        tags:
          - Project
        responses:
          200:
            description: 返回信息
            examples:
              success: {"code": 200,"msg": "success","data": "......."}
        security:
          - basicAuth: []
        """
        # from celery_app.tasks import timer_print
        # timer_print.delay()
        return "success"


class ProjectTestResource(Resource):
    @standard_resp
    @result_to_camel_case
    def get(self):
        """
        test
        ---
        tags:
          - Project
        responses:
          200:
            description: 返回信息
            examples:
              success: {"code": 200,"msg": "success","data": "......."}
        security:
          - basicAuth: []
        """
        logger.info('before sleep')
        time.sleep(50)
        logger.info('after sleep')
        return "success"


class UploadFileResource(Resource):
    method_decorators = [rate_limit]

    @standard_resp
    def post(self):
        base_dir = os.path.dirname(__file__)
        print(base_dir)
        p_base_dir = os.path.dirname(os.path.dirname(base_dir))
        print(p_base_dir)
        file_path = os.path.join(p_base_dir, 'files')
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        # file = request.files.get('file')
        # file.save(os.path.join(file_path, f'save_{file.name}'))
        return 'success'
