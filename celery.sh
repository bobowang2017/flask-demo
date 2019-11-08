#celery multi start w1 -A ext.celery -B -l info --logfile=/var/log/celery.log --pidfile=celerypid.pid
# window10下启动celery用如下命令
#celery -A celery_app worker --pool=solo -l info
ps aux | grep 'celery worker' | awk '{print $2}' | xargs kill -9
celery worker -A app.celery_app --loglevel=info --logfile=/var/log/celery.log --pidfile=celerypid.pid -P eventlet &