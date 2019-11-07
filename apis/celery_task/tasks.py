from exts import celery_app
from celery.utils.log import get_task_logger
# # 创建一个logger对象
logger = get_task_logger(__name__)


@celery_app.task
def timer_print():
    logger.info('*' * 50)
    print('*' * 50)
