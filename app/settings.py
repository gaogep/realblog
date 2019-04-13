import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    # -------------------------------------------------
    BLOG_PER_PAGE = 8
    BLOG_ADMIN_PER_PAGE = 10
    BLOG_COMMENT_PER_PAGE = 15
    # --------------------------------------------------
    BLOG_THEMES = {'bootstrap': '默认', 'lumen': 'lumen'}
    # --------------------------------------------------
    # WHOOSHEE_DIR = 用于配置全局搜索的索引文件夹
    # 设置全文搜索的最小关键字
    WHOOSHEE_MIN_STRING_LEN = 1


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DB')


class ProConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = '...'


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = '...'


config = {'DEV': DevConfig, 'PRO': ProConfig, 'TEST': TestConfig}
