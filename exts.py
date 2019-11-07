# 防止循环引用问题
import logging
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

from settings import CONFIG
from flask_mail import Mail

# 初始化DB
db = SQLAlchemy()
# 初始化邮件
mail = Mail()

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
celery = Celery('celery_app', broker='redis://10.176.139.10:6379/0')
celery.config_from_object('celery_config.CeleryConfig')
