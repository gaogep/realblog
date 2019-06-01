from flask.views import MethodView
from flask import jsonify, request

from ..v1 import api_v1
from .errors import api_abort
from .auth import generate_token, auth_required
from .schemas import category_schema, post_schema
from app.models import Category, Post, User
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
    decorators = [auth_required]

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


class PostAPI(MethodView):
    decorators = [auth_required]

    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return jsonify(post_schema(post))

    # 后续略过....


class AuthTokenAPI(MethodView):
    def post(self):
        grant_type = request.form.get('grant_type')
        username = request.form.get('username')
        password = request.form.get('password')

        if grant_type is None or grant_type.lower() != 'password':
            return api_abort(code=400, message='The grant tpye must be password')

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return api_abort(code=400, message='Either the username or password was invalid')

        token, expiration = generate_token(user)
        response = jsonify({
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': expiration
        })

        response.headers['Cache-control'] = 'no-store'
        response.headers['Pragma'] = 'no-cache'
        return response


api_v1.add_url_rule('/', view_func=IndexApI.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/category/<int:category_id>', view_func=CategoryAPI.as_view('category'), methods=['GET', 'PUT', 'DELETE'])
api_v1.add_url_rule('/post/<int:post_id>', view_func=PostAPI.as_view('post'), methods=['GET', 'PUT', 'DELETE'])
api_v1.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
