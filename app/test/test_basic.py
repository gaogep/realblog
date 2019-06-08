import unittest
from flask import current_app
from app import create_app
from app.extensions import db


class BaseTestCase(unittest.TestCase):
    """
        1.测试App是否存在
        3.测试测试客户端是否启用
        2.测试App是否处在测试配置中
    """
    def setUp(self):
        self.app = create_app('TEST')
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exsit(self):
        self.assertFalse(current_app is None)
        self.assertTrue(self.client)

    def test_app_is_test(self):
        self.assertTrue(current_app.config['TESTING'])
