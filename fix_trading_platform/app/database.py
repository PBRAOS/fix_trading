import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

DATABASE_URL = "postgresql://postgres:Fraoules12@db:5432/db"

# Retry logic for DB connection
max_tries = 10
for i in range(max_tries):

    print('Trying: ', str(i))

    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        print("Connected to PostgreSQL")
        break
    except OperationalError:
        print(f"Database not ready, retrying ({i + 1}/{max_tries})...")
        time.sleep(2) # Make a small pause.
else:
    raise Exception("Database connection failed after retries")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)