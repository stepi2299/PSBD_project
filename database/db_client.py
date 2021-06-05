import psycopg2
from app import config


def making_connection():
    return psycopg2.connect(host=config['DATABASE_HOST'],
                            database=config['DATABASE_NAME'],
                            user=config['DATABASE_USER'],
                            password=config['DATABASE_PASSWORD'],
                            port=config['DATABASE_PORT'])


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
def connect_and_insert_data(command):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = making_connection()

        # creating a cursor
        cur = conn.cursor()

        # execute statement
        cur.execute(command)  # as a parameter SQL code
        print("Successfully executed SQL code")
        cur.close()
        conn.commit()
        print("Successfully inserting new data into database")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

