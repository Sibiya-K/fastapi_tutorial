import os
from dotenv import load_dotenv
from sqlalchemy import create_engine # To create connection to our database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()  # reads .env and loads it into os.environ


# The below is deprecated....
# from sqlalchemy.ext.declarative import declarative_base
# The model is the below...
from sqlalchemy.orm import declarative_base



# Mention our variables, these must not be commited to GitHub

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


# Next we create database URL
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Next we create our connection, using engine
engine = create_engine(DATABASE_URL)

# Create session, that must always be created, at list one session, session maker
# We must get it from Alchemy, by making sure we import it.

SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

# We must stop our session, each time we create a new session, the other must stop first
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   


# Create Base, we must import also, this is where all SQLALchemy will be inherited from
Base = declarative_base()

# Now our database is ready, let's create another file called model.py