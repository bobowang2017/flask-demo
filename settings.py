# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


def test_task():
    print('*' * 30 + 'TimeTrigger' + '*' * 50)


class BaseConfig:
    # 数据库MySQL配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'some secret words')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            'id': 'job_1h_data',
            'func': test_task,
            'args': '',
            'trigger': 'interval',
            'seconds': 20
        }
    ]


class TestingConfig(BaseConfig):
    TESTING = True


class LocalConfig(BaseConfig):
    DEBUG = False
    HOST = 'localhost'
    USERNAME = 'root'
    PASSWORD = 'root'
    PORT = '3333'
    DATABASE = 'devops2.0'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(USERNAME, PASSWORD, HOST, PORT,
                                                                                      DATABASE)
    SQLALCHEMY_ECHO = False


CONFIG = {
    'testing': TestingConfig,
    'local': LocalConfig
}
