from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFError
import click

from .blueprints.main import main_bp
from .blueprints.auth import auth_bp
from .blueprints.admin import admin_bp
from .apis.v1 import api_v1
from .settings import config
from .extensions import *
from .models import *
from .fakes import *


def create_app(conf=None):
    app = Flask(__name__)
    if not conf:
        conf = 'DEV'
    app.config.from_object(config[conf])
    register_blueprints(app)
    register_extensions(app)
    register_shell_context(app)
    register_template_context(app)
    register_errors(app)
    register_commands(app)
    return app


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_v1, url_prefix='/api/v1')


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    csrf.exempt(api_v1)  # 因为api并不使用cookie认证用户 所以取消掉csrf保护
    login_manager.init_app(app)
    moment.init_app(app)
    whooshee.init_app(app)
    toolbar.init_app(app)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Post=Post, Category=Category, Comment=Comment)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        user = User.query.first()
        categories = Category.query.order_by(Category.id).all()
        category_num = len(categories)
        post_num = Post.query.count()
        return dict(user=user, categories=categories, post_num=post_num, category_num=category_num)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    # 根据HTTP内容协商机制来处理由Flask直接处理的错误 用以协调API
    @app.errorhandler(404)
    def page_not_found(e):
        if request.accept_mimetypes.accept_json and \
             not request.accept_mimetypes.accept_html:
            response = jsonify(code=404, message='Not found')
            response.status_code = 404
            return response
        return render_template('errors/404.html'), 404

    @app.errorhandler(405)  # 405错误只发生在API调用中
    def method_not_allowed(e):
        response = jsonify(code=405, message='The method is not allowed for the URL')
        response.status_code = 405
        return response

    @app.errorhandler(500)
    def page_not_found(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html:
            response = jsonify(code=500, message='Internal server error')
            response.status_code = 500
            return response
        return render_template('errors/500.html'), 500

    @app.errorhandler(503)
    def page_not_found(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html:
            response = jsonify(code=503, message='Service unavailable')
            response.status_code = 503
            return response
        return render_template('errors/503.html'), 503

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='生成虚拟分类')
    @click.option('--post', default=50, help='生成虚拟文章')
    @click.option('--comment', default=200, help='生成虚拟评论')
    def build(category, post, comment):
        """生成虚拟数据"""
        db.drop_all()
        db.create_all()
        click.echo('创建用户')
        fake_user()
        click.echo(f'生成{category}种分类...')
        fake_categories(category)
        click.echo(f'生成{post}篇文章...')
        fake_posts(post)
        click.echo(f'生成{comment}条评论...')
        fake_comments(comment)
        click.echo('完成!')
