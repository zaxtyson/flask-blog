from os import path, environ

base_dir = path.abspath(path.dirname(__file__))  # 本文件所在目录的绝对路径


class Config(object):
    """全局配置,安全起见,优先使用环境变量中的值而不将其写在这里"""
    # Flask 配置
    SECRET_KEY = environ.get('SECRET_KEY') or 'II07407CGRLKI4^%&#F'  # Flask 用来加密数据的密匙

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI') or 'sqlite:///' + path.join(base_dir, 'app.db')  # 数据库位置
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用每次更改数据库时通知

    # 邮件服务器配置,用于服务器推送警告信息
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = int(environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    ADMINS = ['zaxtyson@foxmail.com']  # 收件人列表
