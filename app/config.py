from os import path, environ

base_dir = path.abspath(path.dirname(__file__))  # 本文件所在目录的绝对路径


class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY') or 'II07407CGRLKI4^%&#F'  # Flask 用来加密数据的密匙
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'sqlite:///' + path.join(base_dir, 'app.db')  # 数据库位置
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用每次更改数据库时通知
