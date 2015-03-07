# STEP 1: import modules from sqlalchemy to establish the database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://localhost/tbay') # SQLAlchemy way of talking to database - using raw SQL
Session = sessionmaker(bind=engine) # equivalent to psycopg2 cursor. Cue and execute database transactions
session = Session() # NB: can have multiple sessions at a time
Base = declarative_base() # this is a repository for the models and will issue 'create table' statements


# STEP 2: import modules that help create the tables in the database

from datetime import datetime
from decimal import *

from sqlalchemy import Column, Integer, String, DateTime, Float

# create the table 'items' in SQLAlchemy

class Item(Base): # subclass of Base ie 'declarative_base'
    __tablename__ = "items" # used to name the items table in the database

    # four columns in the table
    
    id = Column(Integer, primary_key=True) # an integer primary key used to uniquely id each item
    name = Column(String, nullable=False) # the name of each item, has 'not null' constraint applied
    description = Column(String) # a column for the description of each item
    start_time = Column(DateTime, default=datetime.utcnow) # the auction start time using the DateTime object


# create the table 'user' in SQLAlchemy

class User(Base):
    __tablename__ = "users"

    # three columns in the user table
    
    id = Column(Integer, primary_key=True) # the id of the user and the primary key
    username = Column(String, nullable=False) # the username is a string which can't be null
    password = Column(String, nullable=False) # password for the user, also a string which can't be null


# create the table 'bids' in SQLAlchemy

class Bid(Base):
    __tablename__ = "bids"

    # two columns in the bids table

    id = Column(Integer, primary_key=True) # the id of the bid is the primary key
    price = Column(Float(scale=2), nullable=False) # floating point price which can not be null

    
Base.metadata.create_all(engine)