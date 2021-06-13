import psycopg2
import os
import datetime


def create_tables():
    commands = (
        """
        DROP TABLE IF EXISTS visit, report_comment, report_post, report_user,
                             interest, post, comment, admin_moderator, admin_users,
                             admin_places, attraction, app_user, place, weather,
                             communication, hotel, photo, video, user_groups
        """,
        """
        CREATE TABLE photo (
            id_photo SERIAL PRIMARY KEY,
            name VARCHAR(20),
            file_size REAL,
            file_path VARCHAR(200) NOT NULL,
            extension VARCHAR(10)
        )
        """,
        """
        CREATE TABLE hotel (
            id_hotel SERIAL PRIMARY KEY,
            link VARCHAR(400) NOT NULL,
            km_to_place REAL,
            address_city VARCHAR(100) NOT NULL,
            address_postal_code VARCHAR(200) NOT NULL,
            address_street VARCHAR(100) NOT NULL,
            address_number VARCHAR(10) NOT NULL
        )
        """,
        """
        CREATE TABLE communication (
            id_communication SERIAL PRIMARY KEY,
            link VARCHAR(400) NOT NULL,
            km_to_place REAL,
            type VARCHAR(50) NOT NULL,
            address_city VARCHAR(100) NOT NULL,
            address_latitude VARCHAR(20),
            address_longitude VARCHAR(20)
        )
        """,
        """
        CREATE TABLE attraction (
            id_attraction SERIAL PRIMARY KEY,
            id_photo INTEGER NOT NULL,
            type VARCHAR(50) NOT NULL,
            price REAL,
            description VARCHAR(500),
            open_hours VARCHAR(20) NOT NULL,
            link VARCHAR(200),
            FOREIGN KEY (id_photo)
                REFERENCES photo (id_photo)
        )
        """,
        """
        CREATE TABLE user_groups (
            id_group SERIAL PRIMARY KEY,
            name VARCHAR(40),
            add_places BOOL,
            rm_users BOOL,
            rm_posts BOOL
        )
        """,
        """
        CREATE TABLE app_user (
            login VARCHAR(20) PRIMARY KEY,
            id_photo INTEGER,
            id_group INTEGER NOT NULL,
            name VARCHAR(20),
            surname VARCHAR(20),
            age INTEGER, 
            password_hash VARCHAR(100) NOT NULL,
            creation_date DATE,
            email VARCHAR(50) NOT NULL,
            country VARCHAR(50) NOT NULL,
            FOREIGN KEY (id_photo)
                REFERENCES photo (id_photo),
            FOREIGN KEY (id_group)
                REFERENCES user_groups (id_group)
        )
        """,
        """
        CREATE TABLE place (
            id_place SERIAL PRIMARY KEY,
            id_hotel INTEGER NOT NULL,
            id_communication INTEGER NOT NULL,
            id_attraction INTEGER NOT NULL,
            adding_date DATE,
            localisation_country VARCHAR(50) NOT NULL,
            localisation_region VARCHAR(50) NOT NULL,
            localisation_language VARCHAR(50) NOT NULL,
            localisation_latitude REAL,
            localisation_longitude REAL,
            login_admin VARCHAR(20),
            FOREIGN KEY (id_hotel)
                REFERENCES hotel (id_hotel),
            FOREIGN KEY (id_communication)
                REFERENCES communication (id_communication),
            FOREIGN KEY (id_attraction)
                REFERENCES attraction (id_attraction),
            FOREIGN KEY (login_admin)
                REFERENCES app_user (login)
        )
        """,
        """
        CREATE TABLE weather (
            id_place INTEGER,
            weather_date DATE,
            cloudy VARCHAR(20) NOT NULL,
            humidity REAL,
            temperature REAL,
            FOREIGN KEY (id_place)
                REFERENCES place (id_place),
            CONSTRAINT weather_id PRIMARY KEY (id_place, weather_date)
        )
        """,
        """
        CREATE TABLE comment (
            id_comment SERIAL PRIMARY KEY,
            login VARCHAR(20) NOT NULL,
            add_date DATE,
            content VARCHAR(500) NOT NULL,
            FOREIGN KEY (login)
                REFERENCES app_user (login)
        )
        """,
        """
        CREATE TABLE post (
            id_post SERIAL PRIMARY KEY,
            id_place INTEGER NOT NULL,
            login VARCHAR(20) NOT NULL, 
            id_comment INTEGER NOT NULL,
            add_date DATE,
            id_photo INTEGER NOT NULL,
            review VARCHAR(500),
            FOREIGN KEY (id_place)
                REFERENCES place (id_place),
            FOREIGN KEY (login)
                REFERENCES app_user (login),
            FOREIGN KEY (id_photo)
                REFERENCES photo (id_photo),
            FOREIGN KEY (id_comment)
                REFERENCES comment (id_comment)
        )
        """,
        """
        CREATE TABLE interest (
            id_interest SERIAL PRIMARY KEY,
            id_attraction INTEGER NOT NULL,
            login VARCHAR(20) NOT NULL,
            FOREIGN KEY (id_attraction)
                REFERENCES attraction (id_attraction)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (login)
                REFERENCES app_user (login)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE report_user (
            id_report SERIAL PRIMARY KEY,
            login_admin VARCHAR(20) NOT NULL,
            login VARCHAR(20) NOT NULL,
            add_date DATE,
            reason VARCHAR(500) NOT NULL,
            answer VARCHAR(500) NOT NULL,
            FOREIGN KEY (login)
                REFERENCES app_user (login),
            FOREIGN KEY (login_admin)
                REFERENCES app_user (login)
        )
        """,
        """
        CREATE TABLE report_post (
            id_report SERIAL PRIMARY KEY,
            login VARCHAR(20) NOT NULL,
            id_post INTEGER NOT NULL,
            moderator_login VARCHAR(20) NOT NULL,
            add_date DATE,
            reason VARCHAR(500) NOT NULL,
            answer VARCHAR(500) NOT NULL,
            FOREIGN KEY (login)
                REFERENCES app_user (login),
            FOREIGN KEY (moderator_login)
                REFERENCES app_user (login),
            FOREIGN KEY (id_post)
                REFERENCES post (id_post)
        )
        """,
        """
        CREATE TABLE report_comment (
            id_report SERIAL PRIMARY KEY,
            login VARCHAR(20) NOT NULL,
            id_comment INTEGER NOT NULL,
            admin_login VARCHAR(20) NOT NULL,
            add_date DATE,
            reason VARCHAR(500) NOT NULL,
            answer VARCHAR(500) NOT NULL,
            FOREIGN KEY (login)
                REFERENCES app_user (login),
            FOREIGN KEY (admin_login)
                REFERENCES app_user (login),
            FOREIGN KEY (id_comment)
                REFERENCES comment (id_comment)
        )
        """,
        """
        CREATE TABLE visit (
            arrival_date DATE PRIMARY KEY,
            login VARCHAR(20) NOT NULL,
            id_place INTEGER NOT NULL,
            departure_date DATE,
            FOREIGN KEY (login)
                REFERENCES app_user (login),
            FOREIGN KEY (id_place)
                REFERENCES place (id_place)
        )
        """,
    )
    conn = None

    # references for adding
    photo_sql = """
        INSERT INTO photo(name, file_size, file_path, extension)
        VALUES(%s, %s, %s, %s);
        """
    hotel_sql = """
        INSERT INTO hotel(link, km_to_place, address_city, address_postal_code, address_street, address_number)
        VALUES(%s, %s, %s, %s, %s, %s);
        """
    communication_sql = """
        INSERT INTO communication(link, km_to_place, type, address_city, address_latitude, address_longitude)
        VALUES(%s, %s, %s, %s, %s, %s);
        """
    attractions_sql = """
        INSERT INTO attraction(id_photo, type, price, description, open_hours, link)
        VALUES(%s, %s, %s, %s, %s, %s);
        """
    user_sql = """
        INSERT INTO app_user(login, id_group, id_photo, name, surname, age, password_hash, email, country, creation_date)
        VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s, %s)
        """
    user_group_sql = """
        INSERT INTO user_groups(name, add_places, rm_users, rm_posts)
        VALUES(%s, %s, %s, %s)
        """
    # variables needed to photos to database
    (
        eiffel_photo_name,
        eiffel_photo_path,
        eiffel_photo_size,
        eiffel_photo_ext,
    ) = adding_photo("eiffel_tower.jpg")
    (
        sagrada_photo_name,
        sagrada_photo_path,
        sagrada_photo_size,
        sagrada_photo_ext,
    ) = adding_photo("sagrada_familia.jpg")
    (
        venice_photo_name,
        venice_photo_path,
        venice_photo_size,
        venice_photo_ext,
    ) = adding_photo("venice.jpg")

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="PSBD_places",
            user="postgres",
            password="postgres",
            port=5432,
        )

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        for command in commands:
            cur.execute(command)  # as a parameter SQL code

        # Adding user groups
        cur.execute(user_group_sql, ("user", False, False, False))
        cur.execute(user_group_sql, ("moderator", False, False, True))
        cur.execute(user_group_sql, ("admin places", True, False, False))
        cur.execute(user_group_sql, ("admin users", False, True, True))

        # adding some default photos to sql table "photo"
        cur.execute(
            photo_sql,
            (eiffel_photo_name, eiffel_photo_size, eiffel_photo_path, eiffel_photo_ext),
        )  # eiffel tower
        cur.execute(
            photo_sql,
            (
                sagrada_photo_name,
                sagrada_photo_size,
                sagrada_photo_path,
                sagrada_photo_ext,
            ),
        )  # sagrada familia
        cur.execute(
            photo_sql,
            (venice_photo_name, venice_photo_size, venice_photo_path, venice_photo_ext),
        )  # venice
        # adding some default hotels to sql table "hotel"
        cur.execute(
            hotel_sql,
            (
                "https://www.hotelparisbastille.com/fr/?gclid=Cj0KCQjw8IaGBhCHARIsAGIRRYrNQDqbBua0gWeNK-_Zi6W6JFKC0fgsK3zKxUJ3P7hq_6goqqxWMsYaAggOEALw_wcB",
                1,
                "Paris",
                "75-012",
                "Rue Corzatier",
                "64",
            ),
        )
        cur.execute(
            hotel_sql,
            (
                "https://www.guestreservations.com/novotel-paris-centre-gare-montparnasse/booking?gclid=Cj0KCQjw8IaGBhCHARIsAGIRRYpipawQ3WgkjZbD9vKbEFMZEqryTLSQPqLTTlIUSNHF380-2SbRIvYaAh8DEALw_wcB",
                5,
                "Paris",
                "75-015",
                "Rue de Cotentin",
                "17",
            ),
        )
        cur.execute(
            hotel_sql,
            (
                "https://www.hotelbarcelonaprincess.com/en/?gclid=Cj0KCQjw8IaGBhCHARIsAGIRRYqS4joAX0T4g8M1Nit_el6l7Cq9MnqDADUTNkHmGfIDROhmAr2pevAaAh1yEALw_wcB",
                8,
                "Barcelona",
                "08-019",
                "Sant Marti",
                "1",
            ),
        )
        cur.execute(
            hotel_sql,
            (
                "https://www.booking.com/hotel/it/alloggiagliartistivenezia.pl.html?aid=311264;label=venice-QfIhceaSz2K1nIPll0SohwS390691190566%3Apl%3Ata%3Ap11580%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-1578401895%3Alp9061060%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YbSsBl3MCvHsyw-mWuxZ2N8;sid=a14583ce149d835e3785710b1359fba0;sig=v1OfeuI1Hk",
                3,
                "Venice",
                "30-121",
                "Calle Priuli Cavalletti",
                "99 A/C",
            ),
        )
        # adding some default communications to sql table "communications"
        cur.execute(
            communication_sql,
            (
                "https://www.ratp.fr/en",
                6,
                "Bus",
                "Paris",
                """48° 51' 52.9776'' N""",
                """2° 20' 56.4504'' E""",
            ),
        )
        cur.execute(
            communication_sql,
            (
                "https://www.tmb.cat/en/barcelona-transport/map/bus",
                4,
                "Bus",
                "Barcelona",
                """41° 23' 24.7380'' N""",
                """2° 9' 14.4252'' E""",
            ),
        )
        cur.execute(
            communication_sql,
            (
                "https://www.venicewatertaxi.it/en/",
                7,
                "Water Taxi",
                "Venice",
                """45° 26' 19.5324'' N""",
                """12° 19' 37.7220'' E""",
            ),
        )
        # adding some default attractions to sql table "attractions"

        # adding users
        cur.execute(
            user_sql,
            (
                "kolegakolegi",
                1,
                None,
                "imie",
                "nazwisko",
                89,
                "d32crwsd",
                "kolegakolegi99@wp.pl",
                "pl",
                datetime.datetime.now(),
            ),
        )
        cur.close()
        print("Successfully executed SQL code")
        conn.commit()
        print("Successfully created database's tables instances")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def adding_photo(file_name):
    path = os.path.dirname(__file__)
    photo_path = os.path.join(path, "initial_data", file_name)
    file_size = os.path.getsize(photo_path)
    photo_name, photo_extension = file_name.split(".")
    return photo_name, photo_path, file_size, photo_extension


def making_connection():
    return psycopg2.connect(
        host="localhost",
        database="PSBD_places",
        user="postgres",
        password="postgres",
        port=5432,
    )


def connect_and_pull_users(valid, action="login"):
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        if action == "login":
            command = """
                SELECT * FROM app_user WHERE login = (%s);
                """
        elif action == "email":
            command = """
                SELECT * FROM app_user WHERE email = (%s);
                """
        else:
            print("Wrong action")
            return
        conn = making_connection()

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        cur.execute(command, (valid,))  # as a parameter SQL code
        print("Successfully executed SQL code")
        ret = cur.fetchall()  # returns specified amount of records from database
        print("Successfully getting expected value")
        if ret == []:
            ret = None
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return ret


create_tables()
