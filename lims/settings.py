# -*- coding: utf-8 -*-
PROJECT_NAME = __name__.split('.')[0]


class BaseConfig:
    PROJECT = PROJECT_NAME
    DEBUG = False
    TESTING = False


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(DevConfig):
    TESTING = True
