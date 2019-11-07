from exts import celery
from celery.utils.log import get_task_logger
# # 创建一个logger对象
logger = get_task_logger(__name__)


@celery.task(name='apis.celery_task.tasks.timer_print')
def timer_print():
    logger.info('*' * 50)
