from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, abort, make_response
from flask_login import current_user, login_required

from ..models import Post, Comment, Category
from ..forms import CommentForm
from ..extensions import db
from ..tools import redirect_back


main_bp = Blueprint('main', __name__)


# 以下为两种不同的分页方式
# 主页的分页方式为 -> 将页码写入url
@main_bp.route('/', defaults={'page': 1})
@main_bp.route('/page/<int:page>')
def index(page):
    per_page = current_app.config['BLOG_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('main/index.html', pagination=pagination, posts=posts)


# 分类页面的分页方式为将页面附加到查询字符串中
@main_bp.route('/category/<cate>')
def filter_post(cate):
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_PER_PAGE']
    category = Category.query.filter_by(name=cate).first()
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('main/index.html', pagination=pagination, posts=posts, filter=1, cate=cate)


@main_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.desc()).paginate(page, per_page)
    comments = pagination.items
    form = CommentForm()

    if current_user.is_authenticated:
        from_admin = True
        form.author.data = "张鹏飞"
        form.email.data = "zpf1893@qq.com"
    else:
        from_admin = False

    if form.validate_on_submit():
        author = form.author.data
        content = form.content.data
        comment = Comment(author=author, content=content, post=post, from_admin=from_admin)
        parent_comment_id = request.args.get('reply')
        if parent_comment_id:
            parent_comment = Comment.query.get_or_404(parent_comment_id)
            comment.parent_comment = parent_comment
        db.session.add(comment)
        db.session.commit()
        flash('评论成功', 'success')
        return redirect(url_for('main.show_post', post_id=post_id))
    return render_template('main/post.html', post=post, comments=comments, pagination=pagination, form=form)


@main_bp.route('/comment/delete/<id>', methods=['POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    flash('评论删除成功', 'success')
    return redirect_back()


@main_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(
        url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')


@main_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLOG_THEMES']:
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30*24*60*60)
    return response
