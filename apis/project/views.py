from flask_restful import Resource
from common.helper import standard_resp, result_to_camel_case
from celery_app.tasks import timer_print


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
        timer_print.delay()
        return "success"
