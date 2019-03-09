from functools import wraps

from flask import Markup, flash, url_for, redirect
from flask_login import current_user


def confirm_required(func):
    @wraps
    def decorated_func(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(f"请验证邮箱{url_for('auth.resend_confirm_email')}")
            flash(message, 'warning')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_func
