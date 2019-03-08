from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
import click

from .blueprints.main import main_bp
from .blueprints.auth import auth_bp
from .blueprints.admin import admin_bp
from .settings import config
from .extensions import *
from .models import *
from .fakes import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(config['DEV'])
    register_blueprints(app)
    register_extensions(app)
    register_shell_context(app)
    register_template_context(app)
    # register_errors(app)
    register_commands(app)
    return app


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app) 


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Post=Post, Category=Category, Comment=Comment)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        user = User.query.first()
        categories = Category.query.order_by(Category.id).all()
        return dict(user=user, categories=categories)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='生成虚拟分类')
    @click.option('--post', default=50, help='生成虚拟文章')
    @click.option('--comment', default=200, help='生成虚拟评论')
    def build(category, post, comment):
        """Generates some fake datas"""
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
