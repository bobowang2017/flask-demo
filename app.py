# -*- coding: utf-8 -*-
import json

from flask import Flask, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flasgger import Swagger
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
from apis.project import bp_project
from celery_app import make_celery
from exts import db, config, scheduler
from werkzeug.routing import Map, Rule
from flask_caching import Cache

# 需要传递一个参数__name__
# 1、方便flask框架去寻找资源
# 2、方便flask插件比如Flask-SQLAlchemy出现错误的时候好去寻找问题所在的位置


app = Flask(__name__)

# 添加系统本地缓存
local_cache = Cache(app, config={
    "CACHE_TYPE": "simple"
})

# 注册蓝图
app.register_blueprint(bp_project)

# 加载系统配置
app.config.from_object(config)
# 数据库初始化
db.init_app(app)

celery_app = make_celery(app)

scheduler.init_app(app=app)

# 加载Swagger配置
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/"
}
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "api",
        "description": "Flask-Demo Interface Description",
        "version": "1.0"
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
    # "securityDefinitions": {'basicAuth': {'type': 'basic'}}
    "securityDefinitions": {'basicAuth': {'type': 'apiKey', 'name': 'X-AUTH-TOKEN', 'in': 'header'}},
    "tags": [
        {
            "name": "flask-demo",
            "description": "1.0"
        }
    ],
}
swagger = Swagger(app, config=swagger_config, template=swagger_template)

# migrate
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# 定义免过滤器认证url列表
ignore_url_list = [
    Rule("/api/v1/user/login", methods=["POST"]),
    Rule("/api/v1/users", methods=["GET"]),
    Rule("/api/v1/pipeline/<int:pipeline_id>/callback", methods=["POST"]),
    Rule("/api/v1/pipeline/<int:pipeline_id>/docker/dockerfile", methods=["POST"]),
    Rule("/api/v1/pipeline/<int:pipeline_id>/deploy", methods=["POST"]),
    Rule("/api/v1/websshclient/getcmd/<sshTokenId>", methods=["GET"]),
    Rule("/api/v1/websshclient/check/<sshTokenId>", methods=["GET"]),
    Rule("/api/v1/project/vdc/<string:vdcname>", methods=["GET"]),
    Rule("/api/v1/cluster/account", methods=["POST", "DELETE"])
]

route_map = Map(ignore_url_list)


def check_request(host, path, method):
    urls = route_map.bind(host)
    try:
        urls.match(path_info=path, method=method)
    except Exception:
        return False
    return True


@app.before_request
def handle_chunked():
    """
    解决flask支持分包传输(chunked)问题
    :return:
    """
    transfer_encoding = request.headers.get("Transfer-Encoding")
    if transfer_encoding == "chunked":
        request.environ['wsgi.input_terminated'] = True


@app.before_request
def process_request(*args, **kwargs):
    """
    请求拦截器
    :param args:
    :param kwargs:
    :return:
    """
    # if not request.path.startswith("/api/v1") or check_request(request.host, request.path, request.method):
    #     return
    # user_id = request.headers.get("userId")
    # if not user_id:
    #     return make_response(json.dumps({"code": 404, "msg": msg_const.USER_HEARER_NOT_FOUND_404}), 404)
    # user_info = redis_cli.get("user:" + str(user_id))
    # # 先从缓存查询用户
    # if user_info and not isinstance(user_info, dict):
    #     user_info = json.loads(user_info)
    # 缓存不存在，则查数据库数据
    # if not user_info:
    #     user_info = Serializer.as_dict(user_info)
    #     redis_cli.set("user:" + str(user_id), json.dumps(user_info))
    # setattr(request, 'user_info', user_info)
    pass


socket_list = []


@app.route("/user-msg-task")
def user_msg_task_socket():
    user_socket = request.environ.get("wsgi.websocket")
    socket_list.append(user_socket)
    while True:
        msg = user_socket.receive()
        print(msg)
        try:
            user_socket.send("Hello World")
        except Exception as e:
            print(e)
        for _s in socket_list:
            _s.send(json.dumps({"msg": msg}))


if __name__ == '__main__':
    scheduler.start()
    http_server = WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    # app.run(host="0.0.0.0", debug=False, port=5003)
    # manager.run()
