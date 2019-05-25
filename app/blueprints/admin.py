from flask import Blueprint, flash, redirect, url_for, render_template, request, current_app
from flask_login import login_required, current_user

from ..tools import redirect_back
from ..models import Post, Category
from ..extensions import db
from ..forms import PostWritingForm, CategoryForm

admin_bp = Blueprint('admin', __name__)


# 为admin下的所有视图函数添加登录保护
@admin_bp.before_request
@login_required
def login_protect():
    pass


@admin_bp.route('/manage/post')
def manage_post():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_ADMIN_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('admin/manage_post.html', pagination=pagination, posts=posts)


@admin_bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostWritingForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        title = form.title.data
        category = Category.query.get(form.category.data)
        content = form.content.data
        post = Post(title=title, category=category, content=content, user=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('发布成功', 'success')
        return redirect(url_for('main.show_post', post_id=post.id))
    return render_template('main/mk_editor.html', form=form)


@admin_bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    form = PostWritingForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = Category.query.get(form.category.data)
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash('修改成功', 'success')
        return redirect(url_for('main.show_post', post_id=post.id))
    form.title.data = post.title
    form.category.data = post.category.name
    form.content.data = post.content
    return render_template('main/mk_editor.html', form=form)


@admin_bp.route('/post/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect_back()


@admin_bp.route('/manage/category')
def manage_category():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_ADMIN_PER_PAGE']
    pagination = Category.query.paginate(page, per_page)
    categories = pagination.items
    return render_template('admin/manage_category.html', pagination=pagination, categories=categories)


@admin_bp.route('/category/new', methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category_name = form.category.data
        cname_list = [c.name for c in (Category.query.all())]
        if category_name in cname_list:
            flash('类别重复', 'warning')
            return redirect(url_for('admin.new_category'))
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()
        flash('新建分类成功', 'success')
        return redirect(url_for('main.index'))
    return render_template('admin/build_category.html', form=form)


@admin_bp.route('/category/<category_id>')
def edit_category(category_id):
    category = Category.query.get(category_id)
    form = CategoryForm()
    if form.validate_on_submit():
        category_name = form.category.data
        cname_list = [c.name for c in (Category.query.all())]
        if category_name in cname_list:
            flash('类别重复', 'warning')
            return redirect(url_for('admin.new_category'))
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()
        flash('新建分类成功', 'success')
        return redirect_back()
    form.category.data = category.name
    return render_template('admin/build_category.html', form=form)


@admin_bp.route('/category/delete/<int:category_id>', methods=['POST'])
def delete_categroy(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('无法删除默认分类', 'warning')
        return redirect(url_for('main.index'))
    category.delete()
    flash('分类已删除', 'success')
    return redirect(url_for('admin.manage_category'))
