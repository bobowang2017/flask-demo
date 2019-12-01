# -*- coding: utf-8 -*-
from flask import current_app


def timer_print():
    from apis.project.models import Project
    from exts import logger
    from app import app
    with app.app_context():
        projects = Project.query.all()
        for p in projects:
            logger.info(p.name)
            logger.info(p.code)
    return [{'id': p.id, 'code': p.code, 'name': p.name} for p in projects]
