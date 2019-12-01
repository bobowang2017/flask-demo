# -*- coding: utf-8 -*-
from flask_apscheduler import APScheduler as _BaseAPScheduler


class APScheduler(_BaseAPScheduler):
    def run_job(self, id, jobstore=None):
        with self.app.app_context():
            super().run_job(id=id, jobstore=jobstore)

# https://blog.csdn.net/arnolan/article/details/84936075
