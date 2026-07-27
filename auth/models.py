# Like we created book; we will create user
from sqlalchemy import Column, Integer, String
from auth_database import Base

class User (Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique= True, index=True)
    email = Column(String(255), unique= True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(250), default= "user")

# Next we create schemas.py file