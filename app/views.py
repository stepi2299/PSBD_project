from app import app, login
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from .forms import *
from database.db_client import connect_and_pull_users, register_user
from core.datastructures import User
from werkzeug.security import generate_password_hash
from datetime import datetime


@login.user_loader
def load_user(login):
    return connect_and_pull_users(login)


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


@app.route("/main")
def main_page():
    return render_template("main_page.html", title="Main Page")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user = User(
            login=form.username.data,
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            password_hash=password_hash,
            age=form.age.data,
            id_group=1,
            create_account_date=datetime.now(),
            country=form.country.data,
        )
        register_user(user=user)
        flash("Thanks for registering")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = connect_and_pull_users(valid=username)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            print("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
    return render_template('admin_page.html', title='Admin Page')


@app.route('/admin_page/hotel/', methods=['GET', 'POST'])
def add_hotel():
    form = HotelForm()
    if form.validate_on_submit():
        # tu inserty krystiana sie przydadza
        return redirect(url_for('admin_page'))
    return render_template('add_hotel.html', title='Add Hotel', form=form)


@app.route('/admin_page/attraction/', methods=['GET', 'POST'])
def add_attraction():
    form = AttractionForm()
    if form.validate_on_submit():
        # tu inserty krystiana sie przydadza
        return redirect(url_for('admin_page'))
    return render_template('add_attraction.html', title='Add Attraction', form=form)


@app.route('/admin_page/transport/', methods=['GET', 'POST'])
def add_transport():
    form = TransportForm()
    if form.validate_on_submit():
        # tu inserty krystiana sie przydadza
        return redirect(url_for('admin_page'))
    return render_template('add_transport.html', title='Add Transport', form=form)


@app.route('/admin_page/place/', methods=['GET', 'POST'])
def add_place():
    form = PlaceForm()
    if form.validate_on_submit():
        # tu inserty krystiana sie przydadza
        return redirect(url_for('admin_page'))
    return render_template('add_place.html', title='Add Place', form=form)
