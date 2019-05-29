from flask.views import MethodView
from flask import jsonify, request

from ..v1 import api_v1
from .schemas import category_schema, post_schema
from app.models import Category, Post
from app.extensions import db


class IndexApI(MethodView):
    def get(self):
        return jsonify({
            "api_version": "1.0",
            "api_base_url": "http://example.com/api/v1",
            "current_user_url": "http://example.com/api/v1/user",
            "authenication_url": "http://example.com/api/v1/token",
            "item_url": "http://example.com/api/v1/items/{item_id}",
        })


class CategoryAPI(MethodView):
    def get(self, category_id):
        category = Category.query.get_or_404(category_id)
        return jsonify(category_schema(category))

    def delete(self, category_id):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()

    def put(self, category_id):
        category = Category.query.get_or_404(category_id)
        data = request.get_json()
        new_category = data.get('category')
        category.name = new_category
        db.session.add(category)
        db.session.commit()


class PostApI(MethodView):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return jsonify(post_schema(post))


api_v1.add_url_rule('/', view_func=IndexApI.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/category/<int:category_id>', view_func=CategoryAPI.as_view('category'), methods=['GET', 'PUT', 'DELETE'])
api_v1.add_url_rule('/post/<int:post_id>', view_func=PostApI.as_view('post'), methods=['GET', 'PUT', 'DELETE'])