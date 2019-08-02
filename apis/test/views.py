from flask.views import MethodView
from apis.test import bp_tests
from apis.test.models import User
from exts import db
from tools.redis_api import redis_cli
from flask import current_app


@bp_tests.route('/redis/test', methods=['GET'])
def total():
    total = redis_cli.incr_instance('total')
    return "<h1>The %s Click</h1>" % str(total)


@bp_tests.route('/health', methods=['GET'])
def health():
    return "success"


class TestView(MethodView):
    def get(self):
        user = User(username='admin', password='admin@example.com', sex=1, name='bobo')
        db.session.add(user)
        db.session.commit()
        current_app.logger.debug('A value for debugging')
        return "Success"

    def post(self):
        user = User(username='admin', password='admin@example.com')
        db.session.add(user)
        db.session.commit()
        return "Success"


bp_tests.add_url_rule('tests', view_func=TestView.as_view('tests'))
