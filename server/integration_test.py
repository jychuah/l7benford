import psycopg2
import os
from app import make_connection


def test_postgres():
    conn, cursor = make_connection()
    cursor.execute("SELECT filename FROM benford;")
    row = cursor.fetchone()
    assert row[0] == 'census_2009b'