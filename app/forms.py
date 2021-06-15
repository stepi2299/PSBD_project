from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    SubmitField,
    FileField,
)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, regexp, re
from database.db_client import connect_and_pull_users


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    # image = FileField(u"Image File", [regexp(u"^[^/\\]\.jpg$")])
    country = StringField("Country", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = connect_and_pull_users(valid=username.data)
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = connect_and_pull_users(valid=email.data, action="email")
        if user is not None:
            raise ValidationError("Please use a different email address.")

    """
    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r"[^a-z0-9_.-]", "_", field.data)
    """


class AdminForm(FlaskForm):
    pass
