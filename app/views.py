from app import app, login
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from .forms import *
from database.db_client import *
from core.datastructures import User, Hotel, Attraction, Transport, Place
from werkzeug.security import generate_password_hash
from datetime import datetime


@login.user_loader
def load_user(login):
    return connect_and_pull_users(login)


@app.route("/")
@app.route("/index")
def index():
    return f"Hello, World!"


@app.route("/main")
def main_page():
    photo_places = get_photos_with_param("place")
    pl_len = len(photo_places)
    places = []
    for photo in photo_places:
        places.append(
            {
                "place_name": photo.place_name,
                "id_place": photo.id_place,
                "path": photo.file_path,
            }
        )
    photo_attractions = get_photos_with_param("attraction")
    at_len = len(photo_attractions)
    attractions = []
    for photo in photo_attractions:
        attractions.append(
            {
                "attraction_name": photo.attraction_name,
                "id_place": photo.id_place,
                "path": photo.file_path,
            }
        )
    return render_template(
        "main_page.html",
        title="Main Page",
        places=places,
        attractions=attractions,
        pl_len=pl_len,
        at_len=at_len,
    )


@app.route("/user/<login>")
@login_required
def user(login):
    user = connect_and_pull_users(valid=login)
    # tutaj trzeba będzie jeszcze wyciągnąc jego podróże znajomych itp i przekazac do templatki
    return render_template("user_page.html", title="User Page", user=user)


@app.route("/place/<int:pk>")
def place(pk):
    place = get_places("id_place", pk)[0]
    place_dict = {"place_id": place.id, "name": place.name}
    photo = get_photo(place.id_photo)
    photo = {"path": photo.file_path}
    hotels = get_hotels(pk)
    hotels_list = []
    for hotel in hotels:
        hotels_list.append(
            {
                "name": hotel.name,
                "city": hotel.city,
                "street": hotel.street,
                "number": hotel.house_number,
                "distance": hotel.distance,
                "link": hotel.link,
            }
        )
    transports = get_transport(pk)
    return render_template(
        "place.html",
        title="Place Profile",
        place=place_dict,
        photo=photo,
        hotels=hotels_list,
        transports=transports,
    )


@app.route("/attraction/<int:pk>")
def attraction(pk):
    return render_template("attraction_profile.html", title="Attraction Profile")


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
        return redirect(url_for("main_page"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = connect_and_pull_users(valid=username)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            print("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("main_page"))
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
        places = get_places()
        id_place_help = 0
        for place in places:
            if place.name == HotelForm.city:
                id_place_help = place.id
        distance_help = float(form.distance.data)
        hotel = Hotel(
            city=form.city.data,
            postal_address=form.postal_code.data,
            street=form.street.data,
            house_number=form.house_number.data,
            #TODO didnt know what to do with this id :( (with others too)
            id=None,
            name=form.name.data,
            id_place=id_place_help,
            distance=distance_help,
            link=form.site_link.data,
        )
        add_hotel_to_database(hotel)
        flash("Thanks for adding a hotel!")
        return redirect(url_for('admin_page'))
    return render_template('add_hotel.html', title='Add Hotel', form=form)


@app.route('/admin_page/attraction/', methods=['GET', 'POST'])
def add_attraction():
    form = AttractionForm()
    if form.validate_on_submit():
        places = get_places()
        id_place_help = 0
        for place in places:
            if place.name == HotelForm.city:
                id_place_help = place.id
        price_help = float(form.price.data)
        attraction = Attraction(
            id=None,
            name=form.name.data,
            id_place=id_place_help,
            id_photo=None,
            type=form.type.data,
            description=form.description.data,
            price=price_help,
            open_hours=form.open_hours.data,
            link=form.site_link.data,
        )
        add_attraction_to_database(attraction)
        flash("Thanks for adding an attraction!")
        return redirect(url_for('admin_page'))
    return render_template('add_attraction.html', title='Add Attraction', form=form)


@app.route('/admin_page/transport/', methods=['GET', 'POST'])
def add_transport():
    form = TransportForm()
    if form.validate_on_submit():
        places = get_places()
        id_place_help = 0
        for place in places:
            if place.name == HotelForm.city:
                id_place_help = place.id
        distance_help = float(form.distance.data)
        transport = Transport(
            id=None,
            id_place=id_place_help,
            distance=distance_help,
            link=form.site_link.data,
            type=form.type.data,
            city=form.city.data,
            longitude=form.longitude.data,
            latitude=form.latitude.data,
        )
        add_transport_to_database(transport)
        flash("Thanks for adding a transport!")
        return redirect(url_for('admin_page'))
    return render_template('add_transport.html', title='Add Transport', form=form)


@app.route('/admin_page/place/', methods=['GET', 'POST'])
def add_place():
    form = PlaceForm()
    if form.validate_on_submit():
        place = Place(
            id=None,
            id_photo=None,
            name=form.name.data,
            country=form.country.data,
            region=form.region.data,
            language=form.language.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            #TODO check this (didn't know what to add here)
            admin_login=None,
            create_date=datetime.now(),
        )
        add_place_to_database(place)
        flash("Thanks for adding a place!")
        return redirect(url_for('admin_page'))
    return render_template('add_place.html', title='Add Place', form=form)
