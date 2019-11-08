
from exts import celery_app, db
from celery.utils.log import get_task_logger
# # 创建一个logger对象
logger = get_task_logger(__name__)


@celery_app.task
def timer_print():
    logger.info('*' * 50)
    from app import app
    with app.app_context():
        from apis.project.models import Project
        projects = db.session.query(Project).all()
        for p in projects:
            logger.info(p.name)
            logger.info(p.code)
            logger.info('*' * 50)