def category_schema(category):
    return {
        'category_name': category.name,
        'category_posts': category.posts
    }


def post_schema(post):
    return {
        'title': post.title,
        'body': post.content,
        'date': post.timestamp,
        'category': post.category
    }


def posts_schema(items, current, prev_page, next_page, pagination):
    return {
        'items': [post_schema(post) for post in items],
        'self': current,
        'prev': prev_page,
        'next': next_page,
        'count': pagination.total
    }
