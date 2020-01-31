from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)      # 加载 Flask 配置
db = SQLAlchemy(app)                # 数据库管理对象
migrate = Migrate(app, db)          # 数据库迁移对象
login = LoginManager(app)           # 用户登录管理器
login.login_view = 'login'          # 默认的登录页面('login' 是 routers 中定义的函数名),未登录用户重定向至此

from app import routes, models
