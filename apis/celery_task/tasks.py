from apis.project.models import Project
from exts import celery_app
from celery.utils.log import get_task_logger
# # 创建一个logger对象
logger = get_task_logger(__name__)


@celery_app.task
def timer_print():
    logger.info('*' * 50)
    projects = Project.query.all()
    for p in projects:
        logger.info(p.name)
        logger.info(p.code)
        logger.info('*' * 50)