import psycopg2


def create_tables():
    commands = (
        """
        CREATE TABLE place (
            id_place SERIAL PRIMARY KEY,
            adding_date DATE,
            localisation_country VARCHAR(50) NOT NULL,
            localisation_region VARCHAR(50) NOT NULL,
            localisation_language VARCHAR(50) NOT NULL,
            localisation_latitude REAL,
            localisation_longitude REAL
        )
        """,
        """
        CREATE TABLE hotel (
            id_hotel SERIAL PRIMARY KEY,
            id_place INTEGER NOT NULL,
            link VARCHAR(200) NOT NULL,
            km_to_place REAL,
            address_city VARCHAR(100) NOT NULL,
            address_postal_code VARCHAR(200) NOT NULL,
            address_street VARCHAR(100) NOT NULL,
            address_number VARCHAR(10) NOT NULL,
            FOREIGN KEY (id_place)
                REFERENCES place (id_place)
        )
        """,
        """
        CREATE TABLE communication (
            id_communication SERIAL PRIMARY KEY,
            id_place INTEGER NOT NULL,
            link VARCHAR(200) NOT NULL,
            km_to_place REAL,
            type VARCHAR(20) NOT NULL,
            address_city VARCHAR(100) NOT NULL,
            address_latitude REAL,
            address_longitude REAL,
            FOREIGN KEY (id_place)
                REFERENCES place (id_place)
        )
        """,
        """
        CREATE TABLE weather (
            date DATE PRIMARY KEY,
            id_place INTEGER NOT NULL,
            cloudy VARCHAR(20) NOT NULL,
            humidity REAL,
            temperature REAL,
            FOREIGN KEY (id_place)
                REFERENCES place (id_place)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE attraction (
            id_attraction SERIAL PRIMARY KEY,
            id_place INTEGER NOT NULL,
            type VARCHAR(50) NOT NULL,
            price REAL,
            description VARCHAR(500),
            open_hours VARCHAR(20) NOT NULL,
            link VARCHAR(200),
            FOREIGN KEY (id_place)
                REFERENCES place (id_place)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE app_user (
            login VARCHAR(20) PRIMARY KEY,
            password VARCHAR(20) NOT NULL,
            creation_date DATE,
            email VARCHAR(50) NOT NULL,
            country VARCHAR(50) NOT NULL
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
        CREATE TABLE post (
            id_post SERIAL PRIMARY KEY,
            id_place INTEGER NOT NULL,
            login VARCHAR(20) NOT NULL, 
            add_date DATE,
            review VARCHAR(500),
            FOREIGN KEY (id_place)
                REFERENCES place (id_place),
            FOREIGN KEY (login)
                REFERENCES app_user (login)
        )
        """,
        """
        CREATE TABLE photo (
            id_photo SERIAL PRIMARY KEY,
            id_attraction INTEGER NOT NULL,
            id_post INTEGER NOT NULL,
            login VARCHAR(20) NOT NULL,
            file_size REAL,
            file_path VARCHAR(200),
            file_photo BYTEA,
            FOREIGN KEY (id_attraction)
                REFERENCES attraction (id_attraction)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (id_post)
                REFERENCES post (id_post)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (login)
                REFERENCES app_user (login)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE comment (
            id_comment SERIAL PRIMARY KEY,
            login VARCHAR(20) NOT NULL,
            id_post INTEGER NOT NULL,
            add_date DATE,
            content VARCHAR(500) NOT NULL,
            FOREIGN KEY (login)
                REFERENCES app_user (login),
            FOREIGN KEY (id_post)
                REFERENCES post (id_post)
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
        cur.close()
        print("Successfully executed SQL code")
        cur.close()
        conn.commit()
        print("Successfully created database's tables instances")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


create_tables()