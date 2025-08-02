import pymssql
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy import URL

def run_debug():
    conn = pymssql.connect(
        server="localhost",
        port=1433,
        user="pbraos",
        password="Fr@oules12",
        database="master")

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.databases")
    for row in cursor.fetchall():
        print(row)

    conn.close()

def run_debug_alchemy():

    url_object = URL.create(
        "mssql+pymssql",
        username="pbraos",
        password="Fr@oules12",
        host="localhost",
        database="master")

    # SQLAlchemy connection string using pymssql
    engine = create_engine(url_object)

    # Test the connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sys.databases"))
        for row in result:
            print(row)



def run_debug_alchemy_engine():

    url_object = URL.create(
        "mssql+pymssql",
        username="pbraos",
        password="Fr@oules12",
        host="localhost",
        database="master")

    # SQLAlchemy connection string using pymssql
    engine = create_engine(url_object)
    engine.connect()
    return engine