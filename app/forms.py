from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from flask_pagedown.fields import PageDownField

from .models import User


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20),
                                              Regexp('^[a-zA-Z0-9]*$', message='违法的用户名')])
    password1 = PasswordField('密码', validators=[DataRequired(), Length(1, 20), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    about_me = StringField('个人简介', validators=[DataRequired(), (Length(1, 200))])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已被注册')
        return True

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')
        return True


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 20)])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


class CommentForm(FlaskForm):
    author = StringField('作者', validators=[DataRequired(), Length(1, 20)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 254)])
    content = TextAreaField('评论', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField('提交')


class PostWritingForm(FlaskForm):
    title = StringField('题目', validators=[DataRequired(), Length(1, 200)])
    category = SelectField('请选择分类', coerce=int, default=1)
    content = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('提交')


class CategoryForm(FlaskForm):
    category = StringField('分类', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField('提交')
