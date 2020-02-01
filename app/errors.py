from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    """404错误页面"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误页面"""
    db.session.rollback()   # 数据库错误时回滚
    return render_template("500.html"), 500
