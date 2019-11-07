# -*- coding: utf-8 -*-
import unittest
from app import app
from exts import db


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config[
            'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/devops2.0?charset=utf8mb4"
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()

    def tearDown(self) -> None:
        self.app_ctx.pop()
