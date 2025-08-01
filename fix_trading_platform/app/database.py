import time
from sqlalchemy import create_engine , text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import getpass
import sys
# sys.path.insert(0, '/Users/pbraimakis/PycharmProjects/Azure server Crypto FIX/fix_trading_platform')
### ----------
# # DEBUGGING
# from troubleshooting_mssql import *
# run_debug()
#  # 1. Initiate logging.
# import logging
# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
#
# run_debug_alchemy()


print(getpass.getuser())
if getpass.getuser() == 'pbraimakis':
    # LOCAL MAC
    DATABASE_URL = f"mssql+pymssql://sa:Fraoules12345@localhost:1433/master"
else:
    # DOCKER
    DATABASE_URL = f"mssql+pymssql://sa:Fraoules12345@db:1433/master"

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
        time.sleep(2)
else:
    raise Exception("Database connection failed after retries")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)