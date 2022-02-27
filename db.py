import psycopg2

def connect_to_database():
    return psycopg2.connect(
        "sslmode=disable dbname=postgres user=postgres hostaddr=35.221.45.109"
    )

# Takes a db connection, service name, http response code, performance score, speed index score, and time to interactive value, then inserts it in the stats table
def insert_test(conn, service_name, response_code, score, speed_index_score, tti):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO stats (name, response_code, score, speed_index_score, tti) VALUES (%(service_name)s, %(response_code)s, %(score)s, %(speed_index_score)s, %(tti)s);", {"service_name":service_name, "response_code":response_code, "score":score, "speed_index_score":speed_index_score, "tti":tti})
    conn.commit()
    return

# Takes a db connection and service name and selects most recent test results of specified service
def select_last_test(conn, service_name):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM stats WHERE name=%(service_name)s AND index = (SELECT MAX(index) FROM stats);", {"service_name":service_name})
    conn.commit()
    return

# select all checks for a specified service over the specified time period
