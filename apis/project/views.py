from flask_restful import Resource
from common.helper import standard_resp, result_to_camel_case


# class ProjectResource(Resource):
#
#     @standard_resp
#     @result_to_camel_case
#     def get(self, project_id):
#         """
#         查询项目详情
#         ---
#         tags:
#           - Project
#         parameters:
#           - in: header
#             name : userId
#             type: integer
#             description: 用户id
#             required: true
#           - name: project_id
#             in: path
#             type: integer
#             required: true
#         responses:
#           200:
#             description: 返回信息
#             examples:
#               success: {"code": 200,"msg": "success","data": "......."}
#         security:
#           - basicAuth: []
#         """
#         project_tool = ProjectTool()
#         return project_tool.get_project(project_id)
#
#     @standard_resp
#     def put(self, project_id):
#         """
#         修改项目信息
#         ---
#         tags:
#           - Project
#         parameters:
#           - in: header
#             name : userId
#             type: integer
#             description: 用户id
#             required: true
#           - name: project_id
#             in: path
#             type: integer
#             required: true
#           - in: body
#             name : body
#             description: 修改项目参数
#             schema:
#               $ref: "#/definitions/ProjectUpdate"
#         definitions:
#           ProjectUpdate:
#             type: object
#             properties:
#               name:
#                 type: string
#                 description: name值
#               avatar:
#                 type: string
#                 description: avatar值
#               description:
#                 type: string
#                 description: 描述
#               owner:
#                 type: integer
#                 description: owner_id
#         responses:
#           200:
#             description: 返回信息
#             examples:
#               success: {"code": 200,"msg": "success","data": "......."}
#         security:
#           - basicAuth: []
#         """
#         kwargs = request.json
#         if not kwargs:
#             return "No Data Modify"
#         tool = ProjectTool()
#         tool.update_project(project_id, **kwargs)
#         return "success"
#
#     @standard_resp
#     def delete(self, project_id):
#         """
#         删除项目
#         ---
#         tags:
#           - Project
#         parameters:
#           - in: header
#             name : userId
#             type: integer
#             description: 用户id
#             required: true
#           - name: project_id
#             in: path
#             type: integer
#             required: true
#         responses:
#           200:
#             description: 返回信息
#             examples:
#               success: {"code": 200,"msg": "success","data": "......."}
#         security:
#           - basicAuth: []
#         """
#         project_tool = ProjectTool()
#         project_tool.delete_project(project_id)
#         return "success"


class ProjectListResource(Resource):
    @standard_resp
    @result_to_camel_case
    def get(self):
        """
        查询项目列表
        ---
        tags:
          - Project
        parameters:
          - in: header
            name : userId
            type: integer
            description: 用户id
            required: true
          - name: name_or_code
            in: query
            type: string
            required: false
            description: name或code
          - name: page
            in: query
            type: integer
            default: 1
            description: 查询页数
          - name: limit
            in: query
            type: integer
            default: 10
            description: 每页的数量
        responses:
          200:
            description: 返回信息
            examples:
              success: {"code": 200,"msg": "success","data": "......."}
        security:
          - basicAuth: []
        """
        return
