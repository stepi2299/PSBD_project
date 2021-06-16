import psycopg2
from app import config
from core.datastructures import User


def making_connection():
    return psycopg2.connect(
        host=config["DATABASE_HOST"],
        database=config["DATABASE_NAME"],
        user=config["DATABASE_USER"],
        password=config["DATABASE_PASSWORD"],
        port=config["DATABASE_PORT"],
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
        "hotel": """INSERT INTO hotel(link, 
                                              km_to_place, 
                                              address_city, 
                                              address_postal_code, 
                                              address_street, 
                                              address_number)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_hotel""",
        "communication": """INSERT INTO communication(link,
                                                        km_to_place,
                                                        type,
                                                        address_city,
                                                        address_latitude,
                                                        address_longitude)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_communication""",
        "attraction": """"INSERT INTO attraction(id_photo,
                                                     type,
                                                     price,
                                                     description,
                                                     open_hours,
                                                     link)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_attraction""",
        "place": """"INSERT INTO place(name, 
                                                id_hotel,
                                                id_communication,
                                                id_attraction,
                                                adding_date,
                                                localisation_country,
                                                localisation_region,
                                                localisation_language,
                                                localisation_latitude,
                                                localisation_longitude)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_place""",
        "weather": """INSERT INTO weather(weather_date,
                                                  cloudy,
                                                  humidity,
                                                  temperature)
                            VALUES(%s, %s, %s, %s, %s) RETURNING weather_id""",
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
