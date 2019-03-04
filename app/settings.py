import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DB')


class ProConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = '...'


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = '...'


config = {'DEV': DevConfig, 'PRO': ProConfig, 'TEST': TestConfig}
