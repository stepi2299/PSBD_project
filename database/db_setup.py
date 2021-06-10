import psycopg2
import os


def create_tables():
    commands = (
        """
        DROP TABLE IF EXISTS visit, report_comment, report_post, report_user, interest, post, comment, admin_moderator,
         admin_users, admin_places, attraction, app_user, place, weather, communication, hotel, photo, video
        """,
        """
        CREATE TABLE photo (
            id_photo SERIAL PRIMARY KEY,
            name VARCHAR(20),
            file_size REAL,
            file_path VARCHAR(200) NOT NULL
        )
        """,
        """
        CREATE TABLE hotel (
            id_hotel SERIAL PRIMARY KEY,
            link VARCHAR(200) NOT NULL,
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
            link VARCHAR(200) NOT NULL,
            km_to_place REAL,
            type VARCHAR(20) NOT NULL,
            address_city VARCHAR(100) NOT NULL,
            address_latitude REAL,
            address_longitude REAL
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
            FOREIGN KEY (id_hotel)
                REFERENCES hotel (id_hotel),
            FOREIGN KEY (id_communication)
                REFERENCES communication (id_communication),
            FOREIGN KEY (id_attraction)
                REFERENCES attraction (id_attraction)
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
        CREATE TABLE app_user (
            login VARCHAR(20) PRIMARY KEY,
            id_photo INTEGER NOT NULL,
            password VARCHAR(20) NOT NULL,
            creation_date DATE,
            email VARCHAR(50) NOT NULL,
            country VARCHAR(50) NOT NULL,
            FOREIGN KEY (id_photo)
                REFERENCES photo (id_photo)
        )
        """,
        """
        CREATE TABLE admin_places (
            id_admin SERIAL PRIMARY KEY
        )INHERITS (app_user)
        """,
        """
        CREATE TABLE admin_users (
            id_admin SERIAL PRIMARY KEY
        )INHERITS (app_user)
        """,
        """
        CREATE TABLE admin_moderator (
            id_admin SERIAL PRIMARY KEY
        )INHERITS (app_user)
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
            id_admin INTEGER NOT NULL,
            login VARCHAR(20) NOT NULL,
            add_date DATE,
            reason VARCHAR(500) NOT NULL,
            answer VARCHAR(500) NOT NULL,
            FOREIGN KEY (login)
                REFERENCES app_user (login),
            FOREIGN KEY (id_admin)
                REFERENCES admin_users (id_admin)
        )
        """,
        """
        CREATE TABLE report_post (
            id_report SERIAL PRIMARY KEY,
            login VARCHAR(20) NOT NULL,
            id_post INTEGER NOT NULL,
            id_admin INTEGER NOT NULL,
            add_date DATE,
            reason VARCHAR(500) NOT NULL,
            answer VARCHAR(500) NOT NULL,
            FOREIGN KEY (login)
                REFERENCES app_user (login),
            FOREIGN KEY (id_admin)
                REFERENCES admin_moderator (id_admin),
            FOREIGN KEY (id_post)
                REFERENCES post (id_post)
        )
        """,
        """
        CREATE TABLE report_comment (
            id_report SERIAL PRIMARY KEY,
            login VARCHAR(20) NOT NULL,
            id_comment INTEGER NOT NULL,
            id_admin INTEGER NOT NULL,
            add_date DATE,
            reason VARCHAR(500) NOT NULL,
            answer VARCHAR(500) NOT NULL,
            FOREIGN KEY (login)
                REFERENCES app_user (login),
            FOREIGN KEY (id_admin)
                REFERENCES admin_moderator (id_admin),
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
    photo_sql = (
        """
        INSERT INTO photo(name, file_size, file_path)
        VALUES(%s, %s, %s);
        """
    )
    photo_name, photo_path, photo_size = eiffel_photo()
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="PSBD_places",
            user="postgres",
            password="postgres",
            port=5432)

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        for command in commands:
            cur.execute(command)  # as a parameter SQL code
        cur.execute(photo_sql, (photo_name, photo_size, photo_path))
        cur.close()
        print("Successfully executed SQL code")
        conn.commit()
        print("Successfully created database's tables instances")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def eiffel_photo():
    path = os.path.dirname(__file__)
    photo_path = os.path.join(path, 'initial_data', 'eiffel_tower.jpg')
    file_size = 244.0
    photo_name = 'eiffel tower'
    return photo_name, photo_path, file_size


create_tables()
