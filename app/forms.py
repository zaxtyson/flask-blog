from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
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


class EditProfileForm(FlaskForm):
    """用户信息编辑表单"""
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('关于我', validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('更新个人信息')

    def __init__(self, original_username, *args, **kwargs):
        """表单第一个参数接受原始用户名"""
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """检验用户名是否冲突"""
        if username.data != self.original_username:  # 用户修改了用户名
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('该用户名已被注册 ')
