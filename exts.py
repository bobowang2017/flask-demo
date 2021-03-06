# 防止循环引用问题
import logging
import logging.handlers
import os

from apis.scheduler.scheduler import APScheduler
from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy
from flask_profiler import Profiler
from settings import CONFIG

# 初始化DB
db = SQLAlchemy()

# 初始化flask-profiler
profiler = Profiler()


class FlaskLimiter(object):
    def __init__(self, app):
        self.limiter = Limiter(app)


# 初始化定时器
scheduler = APScheduler()

# 定义日志配置
p_path = os.path.abspath('')
log_path = os.path.join(p_path, 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('logs/log.log', encoding='UTF-8')
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(pathname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
logger.addHandler(handler)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)

# 加载配置类文件
config = CONFIG['local']
