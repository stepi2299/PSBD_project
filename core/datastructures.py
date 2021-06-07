import attr
import datetime


@attr.s
class Image:
    id: int = attr.ib()
    file_size: float = attr.ib()
    file_path: str = attr.ib()


@attr.s
class Video:
    id: int = attr.ib()
    file_size: float = attr.ib()
    file_path: str = attr.ib()
    length: float = attr.ib()
    file_extension: str = attr.ib()


@attr.s
class Localization:
    country: str = attr.ib()
    region: str = attr.ib()
    language: str = attr.ib()
    coordinates: str = attr.ib()  # TODO check if there are coordinates data types


@attr.s
class Weather:
    date: datetime.datetime = attr.ib()
    temperature: float = attr.ib()
    humidity: float = attr.ib()
    cloudy: float = attr.ib()


@attr.s
class Attraction:
    id: int = attr.ib()
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
    distance: float = attr.ib()
    link: str = attr.ib()


@attr.s
class Communication(Address):
    id: int = attr.ib()
    distance: float = attr.ib()
    link: str = attr.ib()
    type: str = attr.ib()


# TODO how to deal with situation when several hotels etc.
@attr.s
class Place(Localization, Weather, Hotel, Communication):
    id: int = attr.ib()
    create_date: datetime.datetime = attr.ib()


@attr.s
class Post:
    id: int = attr.ib()
    create_date: datetime.datetime = attr.ib()
    text: str = attr.ib()
    author_login: str = attr.ib()


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
    report_date = datetime.datetime = attr.ib()
    reason: str = attr.ib()
    post_id: int = attr.ib()
    comment_id: int = attr.ib()
    author_login: str = attr.ib()
    reporter_login: str = attr.ib()


class Visit:
    pass


class User:
    pass


class Interest:
    pass

