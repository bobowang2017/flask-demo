from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://127.0.0.1:6379/1',
        broker='redis://127.0.0.1:6379/0'
    )

    celery.config_from_object('celery_app.celery_config.CeleryConfig')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    setattr(celery, 'Task', ContextTask)
    return celery

