from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)  # 加载 Flask 配置
db = SQLAlchemy(app)  # 数据库管理对象
migrate = Migrate(app, db)  # 数据库迁移对象
login = LoginManager(app)  # 用户登录管理器
login.login_view = 'login'  # 默认的登录页面('login' 是 routers 中定义的函数名),未登录用户重定向至此

# 使用邮件服务推送日志
if not app.debug and app.config['MAIL_SERVER']:
    auth = None
    if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()
    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr=app.config['MAIL_USERNAME'],  # QQ 邮箱要求发件人必须设置为当前用户
        toaddrs=app.config['ADMINS'],
        subject='[服务器错误] Microblog Failure',
        credentials=auth,
        secure=secure
    )
    mail_handler.setLevel(logging.ERROR)  # 只推送 ERROR 级别的日志
    app.logger.addHandler(mail_handler)

# 保存日志文件
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)    # 每个日志 10kb, 保留最近 10个日志
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s [in %(pathname)s:%(lineno)d]: %(message)s'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('-' * 50 + ' Microblog startup ' + '-' * 50)

from app import routes, models, errors
