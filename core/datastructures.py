from werkzeug.security import generate_password_hash, check_password_hash
import attr
import datetime


@attr.s
class Photo:
    id_photo: int = attr.ib()
    name: str = attr.ib()
    file_size: float = attr.ib()
    file_path: str = attr.ib()
    file_extension: str = attr.ib()


@attr.s
class PhotoPlace(Photo):
    id_place: int = attr.ib()
    place_name: str = attr.ib()



@attr.s
class PhotoAttraction(Photo):
    id_place: int = attr.ib()
    attraction_name: str = attr.ib()

@attr.s
class Video:
    id: int = attr.ib()
    file_size: float = attr.ib()
    file_path: str = attr.ib()
    length: float = attr.ib()
    file_extension: str = attr.ib()


@attr.s
class Weather:
    date: datetime.datetime = attr.ib()
    temperature: float = attr.ib()
    humidity: float = attr.ib()
    cloudy: float = attr.ib()
    place_id: int = attr.ib()


@attr.s
class Attraction:
    id: int = attr.ib()
    name: str = attr.ib()
    city: str = attr.ib()
    id_place: int = attr.ib()
    id_photo: int = attr.ib()
    type: str = attr.ib()
    description: str = attr.ib()
    price: float = attr.ib()
    open_hours: str = attr.ib()
    link: str = attr.ib()


@attr.s
class Address:
    city: str = attr.ib()
    postal_address: str = attr.ib()
    street: str = attr.ib()
    house_number: str = attr.ib()


@attr.s
class Hotel(Address):
    id: int = attr.ib()
    name: str = attr.ib()
    id_place: int = attr.ib()
    distance: float = attr.ib()
    link: str = attr.ib()


@attr.s
class Transport:
    id: int = attr.ib()
    id_place: int = attr.ib()
    distance: float = attr.ib()
    link: str = attr.ib()
    type: str = attr.ib()
    city: str = attr.ib()
    # TODO check if there are coordinates data types
    #coordinates: str = attr.ib()
    latitude: str = attr.ib()
    longitude: str = attr.ib()


@attr.s
class Place:
    id: int = attr.ib()
    id_photo: int = attr.ib()
    name: str = attr.ib()
    create_date: datetime.datetime = attr.ib()
    country: str = attr.ib()
    region: str = attr.ib()
    language: str = attr.ib()
    # TODO check if there are coordinates data types
    # coordinates: str = attr.ib()
    latitude: str = attr.ib()
    longitude: str = attr.ib()
    admin_login: str = attr.ib()

@attr.s
class Post:
    id: int = attr.ib()
    create_date: datetime.datetime = attr.ib()
    text: str = attr.ib()
    author_login: str = attr.ib()
    photos_id: set = attr.ib()
    videos_id: set = attr.ib()


@attr.s
class Comment:
    id: int = attr.ib()
    create_date: datetime.datetime = attr.ib()
    text: str = attr.ib()
    author_login: str = attr.ib()
    post_id: int = attr.ib()


# TODO try smart way to do if it is from post or comment
@attr.s
class Reports:
    id: int = attr.ib()
    report_date: datetime.datetime = attr.ib()
    reason: str = attr.ib()
    author_login: str = attr.ib()
    reporter_login: str = attr.ib()


@attr.s
class PostReport(Reports):
    post_id: int = attr.ib()


@attr.s
class CommentReport(Reports):
    comment_id: int = attr.ib()


@attr.s
class Visit:
    arrival_date: datetime.datetime = attr.ib()
    departure_date: datetime.datetime = attr.ib()
    login: str = attr.ib()
    post_id: int = attr.ib()


@attr.s
class User:
    login: str = attr.ib()
    name: str = attr.ib()
    surname: str = attr.ib()
    id_group: int = attr.ib()
    # id_photo: int = attr.ib()
    age: int = attr.ib()
    password_hash: str = attr.ib()
    create_account_date: datetime.datetime = attr.ib()
    email: str = attr.ib()
    country: str = attr.ib()
    is_authenticated = True
    is_active = True
    is_anonymous = True

    def get_id(self):
        return self.login

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@attr.s
class Interest:
    id: int = attr.ib()
    type: str = attr.ib()
