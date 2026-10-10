from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:keerti%401009@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db() :
    db = sessionLocal()
    try : 
        yield db
    finally :
        db.close()


#try:
#    conn = psycopg2.connect(host = 'localhost', database = 'fastapi',user = 'postgres', password = 'keerti@1009', cursor_factory= RealDictCursor)
#    cursor = conn.cursor()
#    print("Database:", conn.info.dbname)
#    print("Host:", conn.info.host)
#    print("Port:", conn.info.port)
#    print("User:", conn.info.user)
#    print("Database connection was succesfull")

#except Exception as error:
#    print("Connecting to database failed")
#    print("Error :", error)
#   time.sleep(2)