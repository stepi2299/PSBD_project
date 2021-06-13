import psycopg2
#from app import config

def making_connection():
    return psycopg2.connect( host="localhost",
            database="PSBD_places",
            user="postgres",
            password="postgres",
            port=5432)


# TODO check if this is working
def connect_and_pull_data(command, return_amount):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = making_connection()

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        cur.execute(command)  # as a parameter SQL code
        print("Successfully executed SQL code")
        cur.fetchmany(return_amount)  # returns specified amount of records from database
        print("Successfully getting expected value")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# TODO check if this is working and how we can pass arguments to insert
def connect_and_insert_data(table_name, value):
    """ Connect to the PostgreSQL database server """
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
        "photo":            """INSERT INTO photo(name, 
                                              file_size, 
                                              file_path)
                            VALUES(%s, %s, %s) RETURNING id_photo"""
        ,
        "hotel":            """INSERT INTO hotel(link, 
                                              km_to_place, 
                                              address_city, 
                                              address_postal_code, 
                                              address_street, 
                                              address_number)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_hotel"""
        ,
        "communication":    """INSERT INTO communication(link,
                                                        km_to_place,
                                                        type,
                                                        address_city,
                                                        address_latitude,
                                                        address_longitude)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_communication"""
        ,
        "attraction":       """"INSERT INTO attraction(id_photo,
                                                     type,
                                                     price,
                                                     description,
                                                     open_hours,
                                                     link)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_attraction"""
        ,
        "place":            """"INSERT INTO place(id_hotel,
                                                id_communication,
                                                id_attraction,
                                                adding_date,
                                                localisation_country,
                                                localisation_region,
                                                localisation_language,
                                                localisation_latitude,
                                                localisation_longitude)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_place"""
        ,
        "weather":          """INSERT INTO weather(weather_date,
                                                  cloudy,
                                                  humidity,
                                                  temperature)
                            VALUES(%s, %s, %s, %s, %s) RETURNING weather_id"""
        ,
        "app_user":         """INSERT INTO app_user(login,
                                                   id_photo,
                                                   password,
                                                   creation_date,
                                                   email,
                                                   country)
                            VALUES(%s, %s, %s, %s, %s, %s)"""
        ,
        "admin_place":      """INSERT INTO admin_place(login,
                                                      id_photo,
                                                      password,
                                                      creation_date,
                                                      email,
                                                      country)
                            VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id_admin"""
        ,
        "admin_moderator":  """INSERT INTO admin_moderator(login,
                                                          id_photo,
                                                          password,
                                                          creation_date,
                                                          email,
                                                          country)
                            VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id_admin"""
        ,
        "comment":          """INSERT INTO comment(login,
                                                  add_date,
                                                  content)
                            VALUES(%s, %s, %s) RETURNING id_comment"""
        ,
        "post":             """INSERT INTO post(id_place,
                                               login,
                                               id_comment,
                                               add_date,
                                               id_photo,
                                               review)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_post"""
        ,
        "interest":         """INSERT INTO interest(id_attraction,
                                                   login)
                            VALUES(%s, %s) RETURNING id_interest"""
        ,
        "report_user":      """INSERT INTO report_user(id_admin,
                                                      login,
                                                      add_date,
                                                      reason,
                                                      answer)
                            VALUES(%s, %s, %s, %s, %s) RETURNING id_report"""
        ,
        "report_post":      """INSERT INTO report_post(login,
                                                      id_post,
                                                      id_admin,
                                                      add_date,
                                                      reason,
                                                      answer)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_report"""
        ,
        "report_comment":   """INSERT INTO report_comment(login,
                                                        id_comment,
                                                        id_admin,
                                                        add_date,
                                                         reason,
                                                         answer)
                            VALUES(%s, %s, %s, %s, %s, %s) RETURNING id_report"""
        ,
        "visit":            """INSERT INTO visit(arrival_date,
                                                login,
                                                id_place,
                                                departure_date)
                            VALUES(%s, %s, %s, %s)"""
    }

    return commands[key]

