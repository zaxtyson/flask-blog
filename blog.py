from app import app, db
from app.models import User, Post

"""
1.进入本文件所在目录，设置环境变量 FLASK_APP = 本文件名 (Windows: set key=value, Linux: export key=value)
2.执行: flask run 启动 Flask
3.执行: flask shell 启动调试 Shell(可以在其中做手动添加、删除用户之类的操作)
"""


@app.shell_context_processor
def make_shell_context():
    """设置 flask shell 自动导入的变量"""
    return {'db': db, 'User': User, 'Post': Post}
