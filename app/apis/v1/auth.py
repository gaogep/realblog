from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, request, g
from functools import wraps

from app.models import User
from .errors import api_abort, token_missing, invalid_token


def generate_token(user):
    """
    生成令牌
    """
    expiration = 3600
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': user.id}).decode('ascii')
    return token, expiration


def get_token():
    """
    因为Flask的request只能处理Basic认证和Digest认证类型的授权字段
    所以我们要自己解析Authorization首部字段以获取令牌值
    """
    token_type = token = None
    if 'Authorization' in request.headers:
        try:
            token_type, token = request.headers['Authorization'].split(None, 1)
        except ValueError:
            pass
    return token_type, token


def validate_token(token):
    """
    验证令牌
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.load(token)
    except (BadSignature, SignatureExpired):
        return False
    user = User.query.get(data['id'])  # 使用令牌中的ID来查询用户对象
    if user is None:
        return False
    g.current_user = user  # 将用户对象存储到g上
    return True


def auth_required(func):
    """
    认证保护装饰器
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        token_type, token = get_token()
        # 由于CORS的缘故 只在OPTIONS之外的请求中调用此装饰器
        if request.method != 'OPTIONS':
            if token_type is None or token_type.lower() != 'bearer':
                return api_abort(400, 'The token type must be bearer')
            if token is None:
                return token_missing()
            if not validate_token(token):
                return invalid_token()
            return func(*args, **kwargs)
    return decorated
