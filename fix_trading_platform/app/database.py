import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import getpass

print(getpass.getuser())
if getpass.getuser() == 'pbraimakis':
    # LOCAL MAC
    DATABASE_URL = "mssql+pyodbc://MySQL:Fr@0ules123!@localhost:1433/db?driver=ODBC+Driver+17+for+SQL+Server"
else:
    # DOCKER
    DATABASE_URL = "mssql+pyodbc://MySQL:Fr@0ules123!@mssql:1433/db?driver=ODBC+Driver+17+for+SQL+Server"

# Retry logic for DB connection
max_tries = 10
for i in range(max_tries):
    print('Trying: ', str(i))
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        print("Connected to SQL Server")
        break
    except OperationalError as e:
        print(f"Database not ready, retrying ({i + 1}/{max_tries})...")
        print(str(e))
        time.sleep(2)
else:
    raise Exception("Database connection failed after retries")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)