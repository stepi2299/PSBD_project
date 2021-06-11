from app import app, login
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from .forms import LoginForm, RegisterForm
from database.db_setup import connect_and_pull_users


@login.user_loader
def load_user(login):
    return connect_and_pull_users(login)


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/main')
def main_page():
    return render_template('main_page.html', title="Main Page")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', title="Register")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = connect_and_pull_users(login=form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))