from flask import Blueprint
from flask_restful import Api

from apis.project.views import (
    ProjectListResource,
    ProjectTestResource
)

bp_project = Blueprint('project', __name__, url_prefix='/api/v1')

api = Api(bp_project)
api.add_resource(ProjectListResource, '/projects')
api.add_resource(ProjectTestResource, '/projects/test')
