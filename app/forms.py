from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    """用户登录表单"""
    username = StringField('用户名', validators=[DataRequired()])      # 可以设置多个验证器，一般 wtforms 库里都有现成的
    password = PasswordField('密码', validators=[DataRequired()])     # 第一个参数是 label
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    """用户注册表单"""
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])     # 使用自带的 Email 验证器验证邮箱地址
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])     # EqualTo 验证两次密码是否相同
    submit = SubmitField('注册')

    # 如果写了任何与 validate_<field_name> 匹配的方法，WTForms 会将这些方法作为自定义的验证器调用, 注意这些方法不能是 staticmethod

    def validate_username(self, name):
        """验证 username """
        user = User.query.filter_by(username=name.data).first()
        if user is not None:
            raise ValidationError('该用户名已被注册')   # 异常携带的 msg 保存在 form.username.errors 这个 list 中, 用于在 html 中提醒用户

    def validate_email(self, email):
        """验证 Email"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱已被注册')
