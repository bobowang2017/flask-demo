from celery.schedules import crontab


class CeleryConfig(object):
    CELERY_BROKER_URL = "redis://10.176.139.10:6379/0"
    CELERY_RESULT_BACKEND = "redis://10.176.139.10:6379/1"
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = True
    CELERYBEAT_SCHEDULE = {
        "test1": {
            "task": "apis.celery_task.tasks.timer_print",  # 执行的函数
            "schedule": crontab(minute="*/1"),  # every minute 每分钟执行
            "args": ()  # # 任务函数参数
        }
    }
    # https://docs.celeryproject.org/en/latest/userguide/configuration.html
