import unittest
from flask import url_for
from app import create_app
from app.extensions import db
from app.fakes import faking


class PageTestCase(unittest.TestCase):
    """
        测试页面显示是否正常
    """
    def setUp(self):
        self.app = create_app('TEST')
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        faking()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        response = self.client.get(url_for('main.index'))
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('张鹏飞的博客', data)
        self.assertIn('文章分类', data)

    def test_read_post(self):
        response = self.client.get(url_for('main.show_post', post_id=1))
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('作者', data)
        self.assertIn('邮箱', data)
        self.assertIn('评论', data)
