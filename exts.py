# 防止循环引用问题
import logging
import logging.handlers
import os
from flask_apscheduler import APScheduler
from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy

from settings import CONFIG

# 初始化DB
db = SQLAlchemy()


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
handler = logging.handlers.TimedRotatingFileHandler('logs/log', 'M', 1, 0)
handler.suffix = "%Y%m%d-%H%M.log"
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(pathname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
logger.addHandler(handler)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)

# 加载配置类文件
config = CONFIG['local']
