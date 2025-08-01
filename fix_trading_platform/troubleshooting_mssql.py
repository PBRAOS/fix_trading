import pymssql
from sqlalchemy import create_engine, text
import urllib

def run_debug():
    conn = pymssql.connect(
        server="localhost",
        port=1433,
        user="sa",
        password="Fraoules12345",
        database="master"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.databases")
    for row in cursor.fetchall():
        print(row)

    conn.close()

def run_debug_alchemy():

    # Connection parameters
    server = "localhost"
    port = 1433
    username = "sa"
    password = "Fraoules12345"
    database = "main"
    quoted_password = urllib.parse.quote_plus(password)

    # SQLAlchemy connection string using pymssql
    engine = create_engine(f"mssql+pymssql://{username}:{quoted_password}@{server}:{port}/{database}")

    # Test the connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sys.databases"))
        for row in result:
            print(row)