import psycopg2


def connect_to_database():
    return psycopg2.connect(
        "sslmode=disable dbname=postgres user=postgres password=JnKDzxuIAJcyvw6A hostaddr=35.221.45.109"
    )


# Takes a db connection, service name, http response code, performance score, speed index score, and time to interactive value, then inserts it in the stats table
def insert_test(conn, service_name, response_code, score, speed_index_score, tti):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO stats (name, response_code, score, speed_index_score, tti) VALUES (%(service_name)s, %(response_code)s, %(score)s, %(speed_index_score)s, %(tti)s);",
            {"service_name": service_name, "response_code": response_code, "score": score,
             "speed_index_score": speed_index_score, "tti": tti})
    conn.commit()
    return


# Takes a db connection and service name and selects most recent test results of specified service
def select_last_test(conn, service_name):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM stats WHERE index = (SELECT MAX(index) FROM stats WHERE name=%(service_name)s);",
                    {"service_name": service_name})
        return cur.fetchone()

# select all checks for a specified service over the specified time period

# select a list of all sites in the sites table
def select_sites(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM sites")
        return cur.fetchall()

