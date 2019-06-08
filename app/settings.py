import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    BLOG_PER_PAGE = 8
    BLOG_ADMIN_PER_PAGE = 10
    BLOG_COMMENT_PER_PAGE = 15

    BLOG_THEMES = {'bootstrap': '默认', 'lumen': 'lumen'}

    # WHOOSHEE_DIR = 用于配置全局搜索的索引文件夹
    # 设置全文搜索的最小关键字
    WHOOSHEE_MIN_STRING_LEN = 1

    # Flask_DebugToolbar关闭拦截重定向请求的特性
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # 调整主机名
    # SERVER_NAME = 'realblog.dev:5000'


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DB')


class ProConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('PRO_DB')


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False  # 测试环境中关闭CSRF保护
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'


config = {'DEV': DevConfig, 'PRO': ProConfig, 'TEST': TestConfig}
