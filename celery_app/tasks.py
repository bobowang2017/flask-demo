from celery.utils.log import get_task_logger
# 创建一个logger对象
from app import celery_app
from flask import current_app
from apis.project.models import Project
from celery_app.base import BaseTask

logger = get_task_logger(__name__)


@celery_app.task
def timer_print():
    app = getattr(current_app, '_get_current_object')()
    with app.app_context():
        projects = Project.query.all()
        for p in projects:
            logger.info(p.name)
            logger.info(p.code)
            logger.info('=' * 50)
        return [{'id': p.id, 'code': p.code, 'name': p.name} for p in projects]


@celery_app.task
def timer():
    logger.info('+' * 50)
