import pymssql
from sqlalchemy import create_engine, text, engine
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
        database="master",
    )

    # SQLAlchemy connection string using pymssql
    engine = create_engine(url_object)

    # Test the connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sys.databases"))
        for row in result:
            print(row)


# Raw pymssql connection function
def get_working_connection():
    return pymssql.connect(
        server="localhost",
        port = 1433,
        user = "sa",
        password = "pAnaGiotis_b",
        database = "main")

def run_injected():
    # Inject into SQLAlchemy using creator
    engine: Engine = create_engine(
        "mssql+pymssql://",  # URL is ignored when using `creator`
        creator=get_working_connection,
        poolclass=StaticPool  # Optional: disables pooling (simpler for local testing)
    )

    # Run a query
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sys.databases"))
        for row in result:
            print(row)