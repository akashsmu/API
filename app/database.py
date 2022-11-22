from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABSE_URL = 'postgresql://postgres:akash@localhost/FastApi'
engine =create_engine(SQLALCHEMY_DATABSE_URL)
sessionlocal = sessionmaker(autocommit= False, autoflush = False ,bind=engine)
Base = declarative_base()

def get_db():
    db= sessionlocal()
    try:
        yield db
    finally:
        db.close()



# while(True):
#     try:
#         conn = psycopg2.connect(host='localhost',database='FastApi',user='postgres',password ='akash', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successfull')
#         break
#     except Exception as error:
#         print('Connecting to database failed', error)
#         time.sleep(2)