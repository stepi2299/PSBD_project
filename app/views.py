from app import app
from flask import render_template
from .forms import LoginForm, RegisterForm


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
