from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import orm
from app import login
from hashlib import md5

# 辅助关联表,不储存数据,只是用来表示用户之间关注和被关注的关系
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


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
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)  # 用户最近一次的活跃时间
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # 用户于帖子之间的关系
    followed = db.relationship(  # 用户与关注/被关注者的关系
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic')

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

    def is_following(self, user):
        """检测用户是否关注另一个用户"""
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        """关注某一个用户"""
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """取消关注某一个用户"""
        if self.is_following(user):
            self.followed.remove(user)

    def followed_posts(self):
        """获取自己和关注的用户发布的帖子"""
        # join 连接 Post 和 followers 表,得到了所有 "有人关注" 的用户发的帖子
        # filter 从中筛选出 follower_id 是当前用户的帖子
        # order_by 将这些帖子按照 timestamp 降序排列
        post_by_followed = Post.query.\
            join(followers, (followers.c.followed_id == Post.user_id)).\
            filter(followers.c.follower_id == self.id)
        post_by_self = Post.query.filter_by(user_id=self.id)
        return post_by_followed.union(post_by_self).order_by(Post.timestamp.desc())


class Post(db.Model):
    """文章数据库模型"""
    id = db.Column(db.INTEGER, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 设置时间戳默认,注意 utcnow 后面没有 ()
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Post {self.id}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
