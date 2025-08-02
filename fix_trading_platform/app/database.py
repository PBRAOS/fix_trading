import time
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import getpass
#import sys
#sys.path.insert(0, '/Users/pbraimakis/PycharmProjects/Azure server Crypto FIX/fix_trading_platform')
## ----------
# DEBUGGING
# from troubleshooting_mssql import *
#run_debug()
# #  # 1. Initiate logging.
# # import logging
#
# # #run_injected()
# #
#run_debug_alchemy()
#
# run_debug_alchemy_engine()

print(getpass.getuser())
if getpass.getuser() == 'pbraimakis':
    # LOCAL MAC
    ## DATABASE_URL = "mssql+pymssql://sa:pAnaGiotis_b@localhost:1433/master"
    url_object = URL.create(
        "mssql+pymssql",
        username="pbraos",
        password="Fr@oules12",
        host="localhost",
        database="master")
else:
    # DOCKER
    ## DATABASE_URL = "mssql+pymssql://sa:pAnagiotis_b@db:1433/master"
    url_object = URL.create(
        "mssql+pymssql",
        username="sa",
        password="pAnagiotis_b",
        host="db",
        database="master")

# Retry logic for DB connection
max_tries = 10
for i in range(max_tries):
    print('Trying: ', str(i))
    try:
        engine = create_engine(url_object)
        engine.connect()
        print("Connected to SQL Server")
        break
    except OperationalError as e:
        print(f"Database not ready, retrying ({i + 1}/{max_tries})...")
        print(e)
        time.sleep(2)
else:
    raise Exception("Database connection failed after retries")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)