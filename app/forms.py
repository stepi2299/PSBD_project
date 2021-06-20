from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    SubmitField,
)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from database.db_client import connect_and_pull_users, get_places, get_hotels
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import photos


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

# TODO checking if the "house number" is a number
class HotelForm(FlaskForm):
    name = StringField("Hotel name", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    postal_code = StringField("Postal Code", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])
    house_number = StringField("Address number", validators=[DataRequired()])
    site_link = StringField("Hotel site link", validators=[DataRequired()]) #soon - change to "not required"
    distance = StringField("Kilometers from center", validators=[DataRequired()]) #idk from where
    submit = SubmitField("Add")

    def no_existing_place(self):
        places = get_places()
        no_place = False
        for place in places:
            if place.name == HotelForm.city:
                no_place = True
        if not no_place:
            raise ValidationError("There is no city named like this.")

    def already_existing_hotel(self):
        places = get_places()
        id_place = 0
        for place in places:
            if place.name == HotelForm.city:
                id_place = place.id
        if id_place != 0:
            hotels = get_hotels(id_place)
            for hotel in hotels:
                if hotel.city == HotelForm.city and hotel.street == HotelForm.street:
                    raise ValidationError("This hotel already exists.")


class AttractionForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    photo = FileField("Photo of attraction", validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
    type = StringField("Type of attratcion", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    open_hours = StringField("Open hours", validators=[DataRequired()])
    site_link = StringField("Attraction site link", validators=[DataRequired()])  # soon - change to "not required"
    submit = SubmitField("Add")


class TransportForm(FlaskForm):
    site_link = StringField("Transport site link", validators=[DataRequired()])  # soon - change to "not required"
    distance = StringField("Kilometers from center", validators=[DataRequired()])  # idk from where
    type = StringField("Type of transport", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    latitude = StringField("Latitude", validators=[DataRequired()])
    longitude = StringField("Longitude", validators=[DataRequired()])
    submit = SubmitField("Add")


class PlaceForm(FlaskForm):
    name = StringField("Place name", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    region = StringField("Region", validators=[DataRequired()])
    language = StringField("Language", validators=[DataRequired()])
    latitude = StringField("Latitude", validators=[DataRequired()])
    longitude = StringField("Longitude", validators=[DataRequired()])
    submit = SubmitField("Add")
