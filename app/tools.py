from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Ser
from itsdangerous import SignatureExpired, BadSignature

from .extensions import db


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='main.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


class Operations:
    CONFIRM = 'mrifnoc'
    RESET_PASSWD = 'dwssapteser'
    CHANGE_EMAIL = 'liameegnahc'


def generate_token(user, operation, expire_in=None, **kwargs):
    s = Ser(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user, token, operation):
    s = Ser(current_app.config['SECRET_KEY'])
    try:
        data = s.load(token)
    except (SignatureExpired, BadSignature):
        return False

    if operation != data.get('operation') or user.id != data.get('id'):
        return False
    if operation == Operations.CONFIRM:
        user.confirmed = True
    else:
        return False

    db.session.commit()
    return True
