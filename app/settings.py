import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    BLOG_PER_PAGE = 8
    BLOG_COMMENT_PER_PAGE = 15

    BLOG_THEMES = {'bootstrap': '默认', 'lumen': 'lumen'}


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DB')


class ProConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = '...'


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = '...'


config = {'DEV': DevConfig, 'PRO': ProConfig, 'TEST': TestConfig}
