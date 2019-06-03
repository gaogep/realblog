from flask.views import MethodView
from flask import jsonify, request, current_app, url_for

from ..v1 import api_v1
from .errors import api_abort
from .auth import generate_token, auth_required
from .schemas import category_schema, post_schema, posts_schema
from app.models import Category, Post, User
from app.extensions import db


class ValidationError(ValueError):
    pass


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

    def put(self, category_id):
        category = Category.query.get_or_404(category_id)
        data = request.get_json()
        new_category = data.get('category')
        category.name = new_category
        db.session.add(category)
        db.session.commit()

    def delete(self, category_id):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()


class PostAPI(MethodView):
    """
    Post单个元素
    """
    decorators = [auth_required]

    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return jsonify(post_schema(post))

    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        data = request.get_json()
        new_content = data.get('content')
        post.content = new_content
        db.session.add(post)
        db.session.commit()

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()


class PostsAPI(MethodView):
    """
     Post资源集合
     """
    decorators = [auth_required]

    def get(self):
        page = request.args.get('page', 1, int)
        per_page = current_app.config['BLOG_PER_PAGE']
        pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page)
        items = pagination.items
        current = url_for('.posts', page=page, _external=True)
        prev_page = None
        if pagination.has_prev:
            prev_page = url_for('.posts', page=page-1, _external=True)
        next_page = None
        if pagination.has_next:
            next_page = url_for('.posts', page=page+1, _external=True)
        return jsonify(posts_schema(items, current, prev_page, next_page, pagination))

    def post(self):
        data = request.get_json()
        title = data.get('title')
        category = data.get('category')
        content = data.get('content')
        post = Post(title=title, category=category, content=content)
        db.session.add(post)
        db.session.commit()
        return jsonify({'success': 'create a new post'})


class AuthTokenAPI(MethodView):
    def post(self):
        grant_type = request.form.get('grant_type')  # 授权类型:密码模式
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

        response.headers['Cache-control'] = 'no-store'  # HTTP/1.1缓存控制:缓存不应存储有关客户端请求或服务器响应的任何内容。
        response.headers['Pragma'] = 'no-cache'         # 用来向后兼容只支持 HTTP/1.0 协议的缓存服务器
        return response


api_v1.add_url_rule('/', view_func=IndexApI.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/categories/<int:category_id>', view_func=CategoryAPI.as_view('category'), methods=['GET', 'PUT', 'DELETE'])
api_v1.add_url_rule('/posts/<int:post_id>', view_func=PostAPI.as_view('post'), methods=['GET', 'PUT', 'DELETE'])
api_v1.add_url_rule('/posts', view_func=PostsAPI.as_view('posts'), methods=['GET'])
api_v1.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
