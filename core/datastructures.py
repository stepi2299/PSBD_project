import attr


@attr.s()
class Image:
    id: int = attr.ib()
    file_size: float = attr.ib()
    file_path: str = attr.ib()


class User:
    pass


class Place:
    pass


class Interest:
    pass


class Attraction:
    pass


class Hotel:
    pass


class Weather:
    pass


class Visit:
    pass


class Post:
    pass


class Video:
    pass


class Comment:
    pass


class Communication:
    pass


class Notification:
    pass
