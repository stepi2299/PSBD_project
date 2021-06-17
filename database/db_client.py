import psycopg2

from app import config
from core.datastructures import User, Place, Attraction, Photo, Transport, Hotel


def making_connection():
    return psycopg2.connect(
        host=config["DATABASE_HOST"],
        database=config["DATABASE_NAME"],
        user=config["DATABASE_USER"],
        password=config["DATABASE_PASSWORD"],
        port=config["DATABASE_PORT"],
    )


def making_connection2():
    return psycopg2.connect(
        host="localhost",
        database="PSBD_places",
        user="postgres",
        password="postgres",
        port=5432,
    )


# TODO check if this is working
def connect_and_pull_data(command, return_amount):
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        conn = making_connection()

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        cur.execute(command)  # as a parameter SQL code
        print("Successfully executed SQL code")
        cur.fetchmany(
            return_amount
        )  # returns specified amount of records from database
        print("Successfully getting expected value")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# TODO check if this is working and how we can pass arguments to insert
def connect_and_insert_data(table_name, value):
    """Connect to the PostgreSQL database server"""
    command = choosing_command(table_name)
    conn = None
    try:
        conn = making_connection()

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        cur.execute(command, value)  # as a parameter SQL code
        print("Successfully executed SQL code")
        cur.close()
        conn.commit()
        print("Successfully inserting new data into database")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def choosing_command(key):
    commands = {
        "photo": """INSERT INTO photo(name, 
                                              file_size, 
                                              file_path, 
                                              extension)
                            VALUES(%s, %s, %s, %s) RETURNING id_photo""",
        "hotel": """INSERT INTO hotel(id_place,link, 
                                              km_to_place, 
                                              address_city, 
                                              address_postal_code, 
                                              address_street, 
                                              address_number)
                            VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id_hotel""",
        "communication": """INSERT INTO communication(id_place, link,
                                                        km_to_place,
                                                        type,
                                                        address_city,
                                                        address_latitude,
                                                        address_longitude)
                            VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id_communication""",
        "attraction": """"INSERT INTO attraction(id_place, id_photo,
                                                     type,
                                                     price,
                                                     description,
                                                     open_hours,
                                                     link)
                            VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id_attraction""",
        "place": """"INSERT INTO place(name, 
                                                id_photo,
                                                adding_date,
                                                localisation_country,
                                                localisation_region,
                                                localisation_language,
                                                localisation_latitude,
                                                localisation_longitude)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_place""",
        "weather": """INSERT INTO weather(id_place, weather_date,
                                                  cloudy,
                                                  humidity,
                                                  temperature)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING weather_id""",
        "app_user": """INSERT INTO app_user(login,
                                                   id_photo,
                                                   id_group,
                                                   name,
                                                   surname,
                                                   age,
                                                   password_hash,
                                                   creation_date,
                                                   email,
                                                   country)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        "comment": """INSERT INTO comment(login,
                                                  add_date,
                                                  content)
                            VALUES(%s, %s, %s) RETURNING id_comment""",
        "post": """INSERT INTO post(id_place,
                                               login,
                                               id_comment,
                                               add_date,
                                               id_photo,
                                               review)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_post""",
        "interest": """INSERT INTO interest(id_attraction,
                                                   login)
                            VALUES(%s, %s) RETURNING id_interest""",
        "report_user": """INSERT INTO report_user(id_admin,
                                                      login,
                                                      add_date,
                                                      reason,
                                                      answer)
                            VALUES(%s, %s, %s, %s, %s) RETURNING id_report""",
        "report_post": """INSERT INTO report_post(login,
                                                      id_post,
                                                      id_admin,
                                                      add_date,
                                                      reason,
                                                      answer)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_report""",
        "report_comment": """INSERT INTO report_comment(login,
                                                        id_comment,
                                                        id_admin,
                                                        add_date,
                                                         reason,
                                                         answer)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_report""",
        "visit": """INSERT INTO visit(arrival_date,
                                                login,
                                                id_place,
                                                departure_date)
                            VALUES(%s, %s, %s, %s)""",
    }

    return commands[key]


def register_user(user):
    connect_and_insert_data(
        "app_user",
        (
            user.login,
            None,
            user.id_group,
            user.name,
            user.surname,
            user.age,
            user.password_hash,
            user.create_account_date,
            user.email,
            user.country,
        ),
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
        user = cur.fetchall()  # returns specified amount of records from database
        print("Successfully getting expected value")
        if user == []:
            user = None
        else:
            user = User(
                login=user[0][0],
                id_group=user[0][2],
                name=user[0][3],
                surname=user[0][4],
                age=user[0][5],
                password_hash=user[0][6],
                create_account_date=user[0][7],
                email=user[0][8],
                country=user[0][9],
            )
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return user


def get_hotels(id_place):
    """Connect to the PostgreSQL database server"""
    command = f"""SELECT *
              FROM hotel
              WHERE '{id_place}' = hotel.id_place
              ORDER BY km_to_place"""
    conn = None
    hotels = []
    try:
        conn = making_connection()

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        cur.execute(command)  # as a parameter SQL code
        print("Successfully executed SQL code")

        row = cur.fetchone()

        while row is not None:
            hotel = Hotel(id=row[0], id_place=row[1], link=row[2], distance=row[3], city=row[4], postal_address=row[5], street=row[6], house_number=row[7])
            hotels.append(hotel)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return hotels  # return list of all hotels connected with pointed place


def get_transport(id_place):
    """Connect to the PostgreSQL database server"""
    command = f"""SELECT *
                 FROM transport
                 WHERE '{id_place}' = transport.id_place
                 ORDER BY km_to_place"""
    conn = None
    means_of_transports = []
    try:
        conn = making_connection()

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        cur.execute(command)  # as a parameter SQL code
        print("Successfully executed SQL code")

        row = cur.fetchone()

        while row is not None:
            transport = Transport(id=row[0], id_place=row[1], link=row[2], distance=row[3], type=row[4], city=row[5], coordinates="")
            means_of_transports.append(transport)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return means_of_transports  # return all means od transport connected with pointed place


def get_photo(id_photo):
    """Connect to the PostgreSQL database server"""
    command = f"""SELECT *
                  FROM photo
                  WHERE '{id_photo}' = photo.id_photo"""
    conn = None
    try:
        conn = making_connection()

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        cur.execute(command)  # as a parameter SQL code
        print("Successfully executed SQL code")

        row = cur.fetchone()
        photo = Photo(id=row[0], name=row[1], file_size=row[2], file_path=row[3], file_extension=row[4])

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return photo  # return single photo selected from db by id


def get_places(column_name=None, attribute_value=None):
    """Connect to the PostgreSQL database server"""
    command = f"""SELECT * FROM place"""
    if column_name is not None and attribute_value is not None:
        command = command + f""" WHERE '{attribute_value}' = place.{column_name}"""

    conn = None
    places = []
    try:
        conn = making_connection()

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        cur.execute(command)  # as a parameter SQL code
        print("Successfully executed SQL code")

        row = cur.fetchone()

        while row is not None:
            place = Place(
                id=row[0],
                id_photo=row[1],
                name=row[2],
                create_date=row[3],
                country=row[4],
                region=row[5],
                language=row[6],
                coordinates="",
                admin_login=row[9],
            )
            places.append(place)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return places  # return list of returned places


def get_attraction(id_place=None):
    """Connect to the PostgreSQL database server"""
    command = f"""SELECT *
                  FROM attraction"""
    if id_place is not None:
        command += f""" WHERE '{id_place}' = attraction.id_place"""
    conn = None
    attractions = []
    try:
        conn = making_connection()

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        cur.execute(command)  # as a parameter SQL code
        print("Successfully executed SQL code")

        row = cur.fetchone()

        while row is not None:
            attraction = Attraction(
                id=row[0],
                id_place=row[1],
                id_photo=row[2],
                type=row[3],
                price=row[4],
                description=row[5],
                open_hours=row[6],
                link=row[7],
            )
            attractions.append(attraction)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return attractions  # return list of returned attractions
