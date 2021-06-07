import psycopg2


def create_tables():
    # Maciek!!! tutaj wewnątrz nawiasów wpisujesz kod SQL odpowiedzialny za stworzenie tabel,
    # asdasdasd
    # tutaj stworzyłem tylko przykłądowa tabelę żebys mógł zobaczyc w jakis sposób
    commands = (
        """
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,)
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