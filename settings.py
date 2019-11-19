# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    # 数据库MySQL配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'some secret words')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379


class TestingConfig(BaseConfig):
    TESTING = True


class LocalConfig(BaseConfig):
    DEBUG = False
    HOST = 'localhost'
    USERNAME = 'root'
    PASSWORD = 'cmdt1234'
    PORT = '3306'
    DATABASE = 'devops2.0'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(USERNAME, PASSWORD, HOST, PORT,
                                                                                      DATABASE)
    SQLALCHEMY_ECHO = False


CONFIG = {
    'testing': TestingConfig,
    'local': LocalConfig
}
