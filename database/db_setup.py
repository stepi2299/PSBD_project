import psycopg2
import os
import datetime
from werkzeug.security import generate_password_hash


def create_tables():
    commands = (
        """
        DROP TABLE IF EXISTS visit, report_comment, report_post, report_user,
                             interest, post, comment, admin_moderator, admin_users,
                             admin_places, attraction, app_user, weather,
                             transport, hotel, photo, video, place, user_groups
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
            password_hash VARCHAR(300) NOT NULL,
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
            id_photo INTEGER NOT NULL,
            name VARCHAR(100),
            adding_date DATE,
            localisation_country VARCHAR(50) NOT NULL,
            localisation_region VARCHAR(50) NOT NULL,
            localisation_language VARCHAR(50) NOT NULL,
            localisation_latitude VARCHAR(20),
            localisation_longitude VARCHAR(20),
            login_admin VARCHAR(20),
            FOREIGN KEY (login_admin)
                REFERENCES app_user (login)
        )
        """,
        """
        CREATE TABLE hotel (
            id_hotel SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            id_place INTEGER,
            link VARCHAR(400) NOT NULL,
            km_to_place REAL,
            address_city VARCHAR(100) NOT NULL,
            address_postal_code VARCHAR(200) NOT NULL,
            address_street VARCHAR(100) NOT NULL,
            address_number VARCHAR(10) NOT NULL,
            FOREIGN KEY (id_place)
                REFERENCES place(id_place)
        )
        """,
        """
        CREATE TABLE transport (
            id_transport SERIAL PRIMARY KEY,
            id_place INTEGER,
            link VARCHAR(400) NOT NULL,
            km_to_place REAL,
            type VARCHAR(50) NOT NULL,
            address_city VARCHAR(100) NOT NULL,
            address_latitude VARCHAR(20),
            address_longitude VARCHAR(20),
            FOREIGN KEY (id_place)
                REFERENCES place(id_place)
        )
        """,
        """
        CREATE TABLE attraction (
            id_attraction SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            id_place INTEGER,
            id_photo INTEGER NOT NULL,
            type VARCHAR(50) NOT NULL,
            price REAL,
            description VARCHAR(500),
            open_hours VARCHAR(20) NOT NULL,
            link VARCHAR(200),
            FOREIGN KEY (id_photo)
                REFERENCES photo (id_photo),
            FOREIGN KEY (id_place)
                REFERENCES place(id_place)
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
        INSERT INTO hotel(name, id_place, link, km_to_place, address_city, address_postal_code, address_street, address_number)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
        """
    transport_sql = """
        INSERT INTO transport(id_place, link, km_to_place, type, address_city, address_latitude, address_longitude)
        VALUES(%s, %s, %s, %s, %s, %s, %s);
        """
    attractions_sql = """
        INSERT INTO attraction(id_place, name, id_photo, type, price, description, open_hours, link)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
        """
    place_sql = """
        INSERT INTO place(
            id_photo,
            name,
            adding_date, 
            localisation_country, 
            localisation_region, 
            localisation_language, 
            localisation_latitude, 
            localisation_longitude,
            login_admin)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
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
    eiffel_photo = adding_photo("eiffel_tower.jpg")
    sagrada_photo = adding_photo("sagrada_familia.jpg")
    gondola_photo = adding_photo("venice.jpg")
    luwr_photo = adding_photo("luwr.jpg")
    camp_nou_photo = adding_photo("camp_nou.jpg")
    wen_arch_photo = adding_photo("wen_arch.jpg")
    paris_photo = adding_photo("Paris.jpg")
    barcelona_photo = adding_photo("barcelona.jpeg")
    venice_photo = adding_photo("wen_arch.jpg")

    password_service = generate_password_hash("service")
    password_moderator = generate_password_hash("moderator")
    password_adminp = generate_password_hash("adminp")
    password_adminu = generate_password_hash("adminu")

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

        # adding users
        cur.execute(
            user_sql,
            (
                "service",
                1,
                None,
                "kolega",
                "kolegi",
                89,
                password_service,
                "kolegakolegi99@wp.pl",
                "pl",
                datetime.datetime.now(),
            ),
        )
        cur.execute(
            user_sql,
            (
                "adminp",
                3,
                None,
                "marek",
                "kiep",
                99,
                password_adminp,
                "marekkiep99@wp.pl",
                "pl",
                datetime.datetime.now(),
            ),
        )
        cur.execute(
            user_sql,
            (
                "moderator",
                2,
                None,
                "remus",
                "romulus",
                99,
                password_moderator,
                "remusromulus@wp.pl",
                "pl",
                datetime.datetime.now(),
            ),
        )
        cur.execute(
            user_sql,
            (
                "adminu",
                4,
                None,
                "szef",
                "ludzi",
                99,
                password_adminu,
                "szef1916@wp.pl",
                "pl",
                datetime.datetime.now(),
            ),
        )

        # adding some default photos to sql table "photo"
        cur.execute(
            photo_sql,
            eiffel_photo,
        )  # eiffel tower
        cur.execute(
            photo_sql,
            (sagrada_photo),
        )  # sagrada familia
        cur.execute(
            photo_sql,
            gondola_photo,
        )  # venice
        cur.execute(
            photo_sql,
            luwr_photo,
        )  # luwr
        cur.execute(photo_sql, camp_nou_photo)  # camp nou
        cur.execute(
            photo_sql,
            wen_arch_photo,
        )  # venice architecture
        cur.execute(photo_sql, paris_photo)
        cur.execute(photo_sql, barcelona_photo)
        cur.execute(photo_sql, venice_photo)
        # adding some places
        cur.execute(
            place_sql,
            (
                7,
                "Paris",
                datetime.datetime.now(),
                "France",
                "Ile-de-France",
                "French",
                """48° 51' 52.9776'' N""",
                """2° 20' 56.4504'' E""",
                "adminp",
            ),
        )  # paris
        cur.execute(
            place_sql,
            (
                8,
                "Barcelona",
                datetime.datetime.now(),
                "Spain",
                "Catalonia",
                "Spanish",
                """41° 23' 24.7380'' N""",
                """2° 9' 14.4252'' E""",
                "adminp",
            ),
        )  # barcelona
        cur.execute(
            place_sql,
            (
                9,
                "Venice",
                datetime.datetime.now(),
                "Italy",
                "Venetia",
                "Italian",
                """45° 26' 19.5324'' N""",
                """12° 19' 37.7220'' E""",
                "adminp",
            ),
        )  # venice

        # adding some default hotels to sql table "hotel"
        cur.execute(
            hotel_sql,
            (
                "Paris Bastille",
                1,
                "https://www.hotelparisbastille.com/fr/?gclid=Cj0KCQjw8IaGBhCHARIsAGIRRYrNQDqbBua0gWeNK-_Zi6W6JFKC0fgsK3zKxUJ3P7hq_6goqqxWMsYaAggOEALw_wcB",
                1,
                "Paris",
                "75-012",
                "Rue Corzatier",
                "64",
            ),
        )  # paris 1
        cur.execute(
            hotel_sql,
            (
                "Novotel Paris Centre",
                1,
                "https://www.guestreservations.com/novotel-paris-centre-gare-montparnasse/booking?gclid=Cj0KCQjw8IaGBhCHARIsAGIRRYpipawQ3WgkjZbD9vKbEFMZEqryTLSQPqLTTlIUSNHF380-2SbRIvYaAh8DEALw_wcB",
                5,
                "Paris",
                "75-015",
                "Rue de Cotentin",
                "17",
            ),
        )  # paris 2
        cur.execute(
            hotel_sql,
            (
                "Barcelona Hotel 1",
                2,
                "https://www.hotelbarcelonaprincess.com/en/?gclid=Cj0KCQjw8IaGBhCHARIsAGIRRYqS4joAX0T4g8M1Nit_el6l7Cq9MnqDADUTNkHmGfIDROhmAr2pevAaAh1yEALw_wcB",
                8,
                "Barcelona",
                "08-019",
                "Sant Marti",
                "1",
            ),
        )  # barcelona 1
        cur.execute(
            hotel_sql,
            (
                "Barcelona hotel 2",
                2,
                "https://www.booking.com/hotel/es/w-barcelona.pl.html",
                4,
                "Barcelona",
                "08-039",
                "Placa Rosa Del Vents",
                "1",
            ),
        )  # barcelona 2
        cur.execute(
            hotel_sql,
            (
                "Venice hotel",
                3,
                "https://www.booking.com/hotel/it/alloggiagliartistivenezia.pl.html?aid=311264;label=venice-QfIhceaSz2K1nIPll0SohwS390691190566%3Apl%3Ata%3Ap11580%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-1578401895%3Alp9061060%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YbSsBl3MCvHsyw-mWuxZ2N8;sid=a14583ce149d835e3785710b1359fba0;sig=v1OfeuI1Hk",
                3,
                "Venice",
                "30-121",
                "Calle Priuli Cavalletti",
                "99 A/C",
            ),
        )  # venice 1
        cur.execute(
            hotel_sql,
            (
                "rio novo venice",
                3,
                "https://www.booking.com/hotel/it/nh-venezia-rio-novo.pl.html",
                5,
                "Venice",
                "30-123",
                "Calle Larga Ragusei Dorsoduro",
                "3489/E-C",
            ),
        )  # venice 2

        # adding some default transport to sql table "transport"
        cur.execute(
            transport_sql,
            (
                1,
                "https://www.ratp.fr/en",
                6,
                "Bus",
                "Paris",
                """48° 51' 52.9776'' N""",
                """2° 20' 56.4504'' E""",
            ),
        )  # paris 1
        cur.execute(
            transport_sql,
            (
                1,
                "https://www.ratp.fr/en",
                4,
                "Metro",
                "Paris",
                """48° 51' 52.9776'' N""",
                """2° 20' 56.4504'' E""",
            ),
        )  # paris 1
        cur.execute(
            transport_sql,
            (
                2,
                "https://www.tmb.cat/en/barcelona-transport/map/bus",
                4,
                "Bus",
                "Barcelona",
                """41° 23' 24.7380'' N""",
                """2° 9' 14.4252'' E""",
            ),
        )  # barcelona 1
        cur.execute(
            transport_sql,
            (
                2,
                "hhttps://www.tmb.cat/en/home",
                2,
                "Metro",
                "Barcelona",
                """41° 23' 24.7380'' N""",
                """2° 9' 14.4252'' E""",
            ),
        )  # barcelona 1
        cur.execute(
            transport_sql,
            (
                3,
                "https://www.venicewatertaxi.it/en/",
                7,
                "Water Taxi",
                "Venice",
                """45° 26' 19.5324'' N""",
                """12° 19' 37.7220'' E""",
            ),
        )  # venice 1
        cur.execute(
            transport_sql,
            (
                3,
                "https://www.veneziaairport.it/en/",
                20,
                "Airport",
                "Venice",
                """45° 26' 19.5324'' N""",
                """12° 19' 37.7220'' E""",
            ),
        )  # venice 2

        # adding some default attractions to sql table "attractions"
        cur.execute(
            attractions_sql,
            (
                1,
                "Eiffel Tower",
                1,
                "Architecture",
                25.60,
                "A wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower.",
                "9:30-23:45",
                "https://www.eiffeltickets.com/?gclid=CjwKCAjwn6GGBhADEiwAruUcKr3cddM0rmN63Hz_UGcu1NIFDrMKGwhSMezmLSW-nLzyV57BEwnkkhoCMi8QAvD_BwE",
            ),
        )  # Paris - eiffel tower
        cur.execute(
            attractions_sql,
            (
                1,
                "Luwr",
                4,
                "Museum",
                17,
                "The world's largest art museum and a historic monument in Paris, France, and is best known for being the home of the Mona Lisa.",
                "9:00-18:00",
                "https://www.louvre.fr/en",
            ),
        )  # Paris - luwr
        cur.execute(
            attractions_sql,
            (
                2,
                "Sagrada de Familia",
                2,
                "Architecture",
                30,
                "Also known as the Sagrada Família, is a large unfinished Roman Catholic minor basilica in the Eixample district of Barcelona, Catalonia, Spain. Designed by the Spanish architect Antoni Gaudí (1852–1926), his work on the building is part of a UNESCO World Heritage Site.[5] On 7 November 2010, Pope Benedict XVI consecrated the church and proclaimed it a minor basilica",
                "9:00-18:00",
                "https://sagradafamilia.org/en/",
            ),
        )  # Barcelona - sagrada familia
        cur.execute(
            attractions_sql,
            (
                2,
                "Camp Nou",
                5,
                "Sport stadium",
                10,
                "A football stadium in Barcelona, Spain. It opened in 1957 and has been the home stadium of FC Barcelona since its completion.",
                "10:00-18:30",
                "https://www.fcbarcelona.com/en/",
            ),
        )  # Barcelona - camp nou
        cur.execute(
            attractions_sql,
            (
                3,
                "Venice channels",
                3,
                "Sightseeing tour",
                22.30,
                "Learn to row like a Venetian! Try the stand-up style made iconic by the gondoliers. You'll support this local tradition with a sustainable activity as you connect with Venice in a rare, traditional Venetian all-wood batella coda di gambero. You can't know Venice if you don’t row Venice!",
                "10:00-19:00",
                "https://www.tripadvisor.com/Attraction_Review-g187870-d1856843-Reviews-Row_Venice-Venice_Veneto.html",
            ),
        )  # Venice - row venice
        cur.execute(
            attractions_sql,
            (
                3,
                "Bazylika Świętego Marka",
                6,
                "Architecture",
                31,
                "A masterpiece of Gothic architecture, the building and its sculptural decoration date from various periods. The interior, with works by artists such as Titian, Veronese, Tintoretto, A.Vittoria and Tiepolo, includes vast council chambers, superbly decorated residential apartments, and austere prison cells.",
                "10:00-18:00",
                "https://www.doge-palace-tickets.com/?gclid=CjwKCAjwwqaGBhBKEiwAMk-FtHL_aWi0ESo0E5ckFQWFoCvk3LZkRZB1XgVx8_ocFXx2310Nm5O9eRoCS-4QAvD_BwE",
            ),
        )  # Venice - doge's palace

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
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(path, "app", "static", "initial_data", file_name)
    photo_path = os.path.join("static", "initial_data", file_name)
    file_size = os.path.getsize(file_path)
    photo_name, photo_extension = file_name.split(".")
    tmp = (photo_name, file_size, photo_path, photo_extension)
    return tmp


def making_connection():
    return psycopg2.connect(
        host="localhost",
        database="PSBD_places",
        user="postgres",
        password="postgres",
        port=5432,
    )


create_tables()
