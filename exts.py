# 防止循环引用问题
import logging
from celery.schedules import crontab
from flask_sqlalchemy import SQLAlchemy
from flask_celery import Celery

from settings import CONFIG

# 初始化DB
db = SQLAlchemy()

# 定义日志配置
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('log.log', encoding='UTF-8')
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(pathname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
logger.addHandler(handler)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)

# 加载配置类文件
config = CONFIG['local']


# 初始化celery
# class MyCelery(Celery):
#     def now(self):
#         """Return the current time and date as a datetime."""
#         from datetime import datetime
#         return datetime.now(self.timezone)


# celery_app = MyCelery('celery_app', broker='redis://127.0.0.1:6379/0')

celery_app = Celery()
celery_app.config_from_object('celery_config.CeleryConfig')
celery_app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'apis.celery_task.tasks.timer_print',
        'schedule': crontab(),
        'args': ()
    },
}
