from flask import Blueprint, flash, redirect, url_for, render_template, request, current_app
from flask_login import login_required, current_user

from ..tools import redirect_back
from ..models import Post, Category
from ..extensions import db
from ..forms import PostWritingFrom

admin_bp = Blueprint('admin', __name__)


# 为admin下的所有视图函数添加登录保护
@admin_bp.before_request
@login_required
def login_protect():
    pass


@admin_bp.route('/post/manage')
def manage_post():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_ADMIN_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('admin/manage_post.html', pagination=pagination, posts=posts)


@admin_bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostWritingFrom()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        title = form.title.data
        category = Category.query.get(form.category.data)
        content = form.pagedown.data
        post = Post(title=title, category=category, content=content, user=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('发布成功', 'success')
        return redirect(url_for('main.show_post', post_id=post.id))
    return render_template('main/mk_editor.html', form=form)


@admin_bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    form = PostWritingFrom()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    form.title.data = post.title
    form.category.data = post.category.name
    form.pagedown.data = post.content
    if form.validate_on_submit():
        title = form.title.data
        category = Category.query.get(form.category.data)
        content = form.pagedown.data
        post = Post(title=title, category=category, content=content, user=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('修改成功', 'success')
        return redirect(url_for('main.show_post', post_id=post.id))
    return render_template('main/mk_editor.html', form=form)


@admin_bp.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect_back()
