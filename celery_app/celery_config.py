from datetime import timedelta

from celery.schedules import crontab


class CeleryConfig(object):
    CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = True
    CELERYBEAT_SCHEDULE = {
        "test1": {
            "task": "celery_app.tasks.timer_print",  # 执行的函数
            'schedule': timedelta(seconds=20),  # every minute 每分钟执行
            "args": ()  # # 任务函数参数
        },
        "test2": {
            "task": "celery_app.tasks.timer",  # 执行的函数
            'schedule': crontab(minute=0, hour=0),  # every minute 每分钟执行
            "args": ()  # # 任务函数参数
        },
    }
    CELERY_IMPORTS = ('celery_app.tasks',)

    # https://docs.celeryproject.org/en/latest/userguide/configuration.html
