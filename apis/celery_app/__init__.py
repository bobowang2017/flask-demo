from celery import Celery
from celery.schedules import crontab

celery_app = Celery()
celery_app.config_from_object('celery_config.CeleryConfig')
celery_app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'apis.celery_task.tasks.timer_print',
        'schedule': crontab(),
        'args': ()
    },
}
