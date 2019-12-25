from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://127.0.0.1:6379/1',
        broker='redis://127.0.0.1:6379/0'
    )

    celery.config_from_object('celery_app.celery_config.CeleryConfig')
    # logger.info(celery.conf.table(with_defaults=False, censored=True))

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            logger.info('task starting: {0.name}[{0.request.id}]'.format(self))
            with app.app_context():
                return self.run(*args, **kwargs)

        def on_success(self, retval, task_id, args, kwargs):
            logger.info('task:{} execute success(args={}, kwargs={})'.format(task_id, args, kwargs))

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            logger.info('task:{} execute failed(args={}, kwargs={})'.format(task_id, args, kwargs))

    setattr(celery, 'Task', ContextTask)
    return celery
