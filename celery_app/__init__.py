from celery import Celery

celery_app = Celery(broker='redis://127.0.0.1:6379/0')
celery_app.config_from_object('celery_config.CeleryConfig')

