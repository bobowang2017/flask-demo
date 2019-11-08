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

        def on_success(self, retval, task_id, args, kwargs):
            print('success')
            print(task_id)

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            print('failure')
            print('{0!r} failed: {1!r}'.format(task_id, exc))

    setattr(celery, 'Task', ContextTask)
    return celery
