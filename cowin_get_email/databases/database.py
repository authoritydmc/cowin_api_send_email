from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, sql
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()
print("database init")


class User(Base):
    __tablename__ = "USER"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    phone = Column('phone', String)
    email = Column('email', String, unique=True)
    age = Column('age', Integer, default=0)
    pincode = Column('pincode', Integer, default=0)
    dist_id = Column('dist_id', Integer, default=0)
    dist_name = Column('dist_name', String, default="NA")
    registered = Column('registered', DateTime, default=datetime.now)
    search_by = Column('search_by', String)


engine = create_engine("sqlite:///db.sqlite3", echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


def addUser(name, age, email, phone, pincode, dist_id, search_by):

    user = User()
    user.name = name
    user.age = age
    user.phone = phone
    user.email = email
    user.search_by = search_by
    user.pincode = pincode
    user.dist_id = dist_id
    session.add(user)
    session.commit()


def getUser():
    pass


def CloseSession():

    session.close()
