# -*- coding: utf-8 -*-
import celery


class BaseTask(celery.Task):

    def on_success(self, retval, task_id, args, kwargs):
        print(task_id)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))
