from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


class User(UserMixin, db.Model):
    """用户数据库模型
    继承 UserMixin 是为了使得 flask-login 能够记录 User 对象的登录状态
    继承 db.Model 是为了 SQLAlchemy 能够管理用户数据
    """
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)     # 用户最近一次的登录时间
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        """print(User)时输出的内容"""
        return f"<User {self.username}>"

    def set_password(self, password):
        """计算明文密码的 hash,存入数据库"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """检测明文密码是否与 hash 对应,用于登录检测"""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """获取用户头像链接
        参数详情: https://gravatar.com/site/implement/images
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Post(db.Model):
    """文章数据库模型"""
    id = db.Column(db.INTEGER, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # 设置时间戳默认,注意 utcnow 后面没有 ()
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Post {self.id}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
