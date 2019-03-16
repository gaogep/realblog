from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from ..forms import LoginForm, RegisterForm
from ..models import User
from ..tools import redirect_back, Operations, generate_token, validate_token
from ..extensions import db
from ..emails import send_email


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit() and \
            form.validate_username(form.username) and form.validate_email(form.email):
        username = form.username.data
        password = form.password1.data
        email = form.email.data.lower()
        about_me = form.about_me.data
        user = User(username=username, email=email, about_me=about_me)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user, Operations.CONFIRM)
        confirm_url = url_for('auth.confirm', token=token, _external=True)
        body = f'请点击这个链接{confirm_url}验证你的邮箱地址'
        send_email('请验证你的邮箱地址', email, body)
        flash('注册成功, 验证邮件已发送至你的邮箱', 'success')
    return render_template('auth/register.html', form=form)


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    # if current_user.confirmed:
    #     return redirect(url_for('main.index'))

    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('验证成功', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('令牌已过期，请重新验证', 'danger')
        return redirect(url_for('auth.resend_confirmation'))


@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    # if current_user.confirmed:
    #     return redirect(url_for('main.index'))
    token = generate_token(current_user, Operations.CONFIRM)
    confirm_url = url_for('auth.confirm', token=token, _external=True)
    body = f'请点击这个链接{confirm_url}验证你的邮箱地址'
    send_email('请验证你的邮箱地址', current_user.email, body)
    flash('新的验证邮件已经发送，请去邮箱确认', 'success')
    return redirect(url_for('main.index'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember)
            flash('登录成功', 'success')
            redirect_back()
        else:
            flash('登录失败', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已登出', 'success')
    return redirect_back()
