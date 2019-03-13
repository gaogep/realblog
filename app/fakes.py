import random
from faker import Faker
from sqlalchemy.exc import IntegrityError

from .models import *
from .extensions import db

fake = Faker(locale='zh_CN')


def fake_user():
    user = User(is_admin=True, username='AdminZpf', about_me='天坑专业自救中...', confirmed=True)
    user.set_password('123654Zz')
    db.session.add(user)
    db.session.commit()


def fake_categories(cnt=10):
    category = Category(name='默认')
    db.session.add(category)
    for i in range(cnt):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(cnt=50):
    category_nums = Category.query.count()
    user_nums = User.query.count()
    for i in range(cnt):
        post = Post(title=fake.sentence(),
                    user=User.query.get(1),
                    content=fake.text(1000),
                    category=Category.query.get(random.randint(1, category_nums)),
                    timestamp=fake.date_time_this_year())
        db.session.add(post)
    db.session.commit()


def fake_comments(cnt=200):
    post_nums = Post.query.count()
    for i in range(cnt):
        comment = Comment(author=fake.name(),
                          content=fake.sentence(),
                          timestamp=fake.date_time_this_year(),
                          post=Post.query.get(random.randint(1, post_nums)))
        db.session.add(comment)

    for i in range(30):
        comment = Comment(author=User.query.first().username,
                          content=fake.sentence(),
                          from_admin=True,
                          timestamp=fake.date_time_this_year(),
                          post=Post.query.get(random.randint(1, post_nums)))
        db.session.add(comment)
    db.session.commit()

    comment_nums = Comment.query.count()
    for i in range(int(cnt >> 2)):
        parent_comment = Comment.query.get(random.randint(1, comment_nums))
        comment = Comment(author=fake.name(),
                          content=fake.sentence(),
                          timestamp=fake.date_time_this_year(),
                          parent_comment=parent_comment,
                          post=Post.query.get(parent_comment.post_id))
        db.session.add(comment)
    db.session.commit()
