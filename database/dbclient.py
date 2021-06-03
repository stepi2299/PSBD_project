import psycopg2


def connect():
    """ Connect to the PostgreSQL database server """
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
        cur.execute('SELECT version()')  # as a parameter SQL code
        ret = cur.fetchone()  # it returns one record from database
        #cur.fetchmany(3)  # returns 3 records from database
        print(ret)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
