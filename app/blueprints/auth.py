from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required

from ..forms import LoginForm
from ..models import User
from ..tools import redirect_back


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember)
            flash('登录成功', 'success')
            return "<h1>欢迎</h1>"
        else:
            flash('登录失败', 'warning')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已登出', 'success')
    return redirect_back()
