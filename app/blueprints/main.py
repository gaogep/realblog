from flask import Blueprint, render_template,request, current_app

from ..models import Post

main_bp = Blueprint('main', __name__)


@main_bp.route('/', defaults={'page': 1})
@main_bp.route('/page/<int:page>')
def index(page):
    per_page = current_app.config['BLOG_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('main/index.html', pagination=pagination, posts=posts)


@main_bp.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('main/post.html', post=post)
