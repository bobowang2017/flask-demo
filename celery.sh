#celery multi start w1 -A ext.celery -B -l info --logfile=/var/log/celery.log --pidfile=celerypid.pid
celery worker -A ext.celery --loglevel=info --logfile=/var/log/celery.log