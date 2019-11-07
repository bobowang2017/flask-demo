#celery multi start w1 -A ext.celery -B -l info --logfile=/var/log/celery.log --pidfile=celerypid.pid
ps aux | grep 'celery worker' | awk '{print $2}' | xargs kill -9
celery worker -A exts.celery_app --loglevel=info --logfile=/var/log/celery.log --pidfile=celerypid.pid -P eventlet