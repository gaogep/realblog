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
