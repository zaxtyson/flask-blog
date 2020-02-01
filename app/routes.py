from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import logout_user, login_user, current_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    """更新登录用户的活跃时间"""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required  # 指定该页面需要登录才能访问,未登录的用户跳转至 login.login_view 设置的页面
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='主页', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if current_user.is_authenticated:  # 如果当前用户认证通过,返回主页
        return redirect(url_for('index'))  # url_for('func_name') 返回该函数的路由地址(因为地址可能经常变动,但是函数名比较稳定)

    form = LoginForm()  # 登录表单对象,验证数据合法性,记录数据值
    if form.validate_on_submit():  # 如果用户提交了该表单,并且数据合法
        user = User.query.filter_by(username=form.username.data).first()  # 从数据库获取用户对象
        if not user or not user.check_password(form.password.data):  # 没有该用户或密码 hash 校验失败
            flash(f"Invalid username or password")  # 向 Flask 的消息队列写入信息,可以通过 get_flashed_messages() 获取消息 list
            return redirect(url_for('index'))

        login_user(user, remember=form.remember_me.data)  # 登录成功,通过 LoginManager 管理 user 在浏览器中的登录状态

        # 用户直接访问的页面 raw_url 可能要求登录,于是跳转到登录页面 /login?next=raw_url
        # next 参数记录用户原始访问的页面,如果没有或者是站外链接就返回主页
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='登录页面', form=form)


@app.route('/logout')
def logout():
    """用户登出"""
    logout_user()  # LoginManager 将用户从浏览器 cookie 中删除
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if current_user.is_authenticated:   # 如果用户已经是登录状态,返回主页
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)    # 向数据库添加用户
        db.session.commit()
        flash('注册成功!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册页面', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    """个人中心页"""
    user = User.query.filter_by(username=username).first_or_404()   # 没有找到用户,抛出异常,返回 404 页面
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """编辑用户信息页"""
    form = EditProfileForm(current_user.username)
    if request.method == 'GET':   # 直接访问时，设置表单默认状态
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    elif form.validate_on_submit():   # 表单验证通过后更新数据库
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("个人信息更新成功")
        return redirect(url_for('edit_profile'))

    return render_template('edit_profile.html', title='更新用户信息', form=form)