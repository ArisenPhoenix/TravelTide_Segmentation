from urllib.parse import urlparse
import sqlalchemy as sal
import psycopg2


"""
Provides A Way To Create Connections To Postgresql Databases For Other Modules To Use.
"""


def get_sql_data(url: str):
    creds = urlparse(url)
    username = creds.username
    password = creds.password
    database = creds.path[1:]
    host = creds.hostname
    port = creds.port
    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=host,
        port=port,
        sslmode="require"
    )
    cursor = conn.cursor()
    return conn


def get_sql_connection(uri):
    eng = sal.create_engine(uri, connect_args={'sslmode': "allow"})
    return eng


