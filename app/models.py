from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from markdown import markdown
import bleach

from .extensions import db, whooshee


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.Text)
    confirmed = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', back_populates='category')

    # 删除一个分类的时候把这个分类中的文章全部移到默认分类中
    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


@whooshee.register_model('title')
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)  # 开启索引用于全文搜索
    content = db.Column(db.Text)
    html_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


@db.event.listens_for(Post.content, 'set', named=True)
def on_chenge_content(**kwargs):
    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'br', 'blockquote', 'code', 'del',
                    'em', 'img', 'p', 'pre', 'strong', 'span', 'li', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'div']
    # linkify函数->将纯文本中的url转换为合适的<a>链接
    kwargs['target'].html_content = bleach.linkify(bleach.clean(
        markdown(kwargs['value'], output_format='html',
                 extensions=['markdown.extensions.toc', 'markdown.extensions.fenced_code']), tags=allowed_tags))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    content = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_admin = db.Column(db.Boolean, default=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    parent_comment = db.relationship('Comment', back_populates='child_comment', remote_side=[id])
    child_comment = db.relationship('Comment', back_populates='parent_comment', cascade='all, delete-orphan')
