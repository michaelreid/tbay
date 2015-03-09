# STEP 1: import modules from sqlalchemy to establish the database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://action:action@localhost:5432/tbay') # SQLAlchemy way of talking to database - using raw SQL
Session = sessionmaker(bind=engine) # equivalent to psycopg2 cursor. Cue and execute database transactions
session = Session() # NB: can have multiple sessions at a time
Base = declarative_base() # this is a repository for the models and will issue 'create table' statements


# STEP 2: import modules that help create the tables in the database

from datetime import datetime
from decimal import * 
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
# remember to import relationship model and ForeignKey
from sqlalchemy.orm import relationship


# create the model table 'items' in SQLAlchemy
class Item(Base): # subclass of Base ie 'declarative_base'
    __tablename__ = "items" # used to name the items table in the database

    # columns describing the items
    id = Column(Integer, primary_key=True) # an integer primary key used to uniquely id each item
    name = Column(String, nullable=False) # the name of each item, has 'not null' constraint applied
    description = Column(String) # a column for the description of each item
    start_time = Column(DateTime, default=datetime.utcnow) # the auction start time using the DateTime object
    # column describing the relationship to users [one(user)-to-many(items)]
    owner = Column(Integer, ForeignKey('users.id'), nullable=False)

# create the model table 'user' in SQLAlchemy
class User(Base):
    __tablename__ = "users"

    # three columns in the user table
    id = Column(Integer, primary_key=True) # the id of the user and the primary key
    username = Column(String, nullable=False) # the username is a string which can't be null
    password = Column(String, nullable=False) # password for the user, also a string which can't be null
    # add relationship details so that users can auction many items [one(users)-to-many(items)]
    items_selling = relationship("Item", backref="items")


# create the model table 'bids' in SQLAlchemy
class Bid(Base):
    __tablename__ = "bids"

    # two columns in the bids table
    id = Column(Integer, primary_key=True) # the id of the bid is the primary key
    price = Column(Float(scale=2), nullable=False) # floating point price which can not be null
    

# STEP 3: create the many-to-many relationship between users and items they're selling
# users_items = Table('users_items', Base.metadata,
#     Column('user_id', Integer, ForeignKey('user.id')),
#     Column('item_id', Integer, ForeignKey('item.id'))
# )

    
# WORKING WITH MODELS 
# some example code to use with working with database
# This could also be written as: michael = User(username="michaelreid", password="password")    
    
# SQLAlchemy creates a default __init__ method for models

# # add michael username
# michael = User()
# michael.username = "michaelreid"
# michael.password = "password"
# session.add(michael)

# # add reid username
# reid = User(username="reid", password="1234")
# session.add(reid)

# # add item one
# item1 = Item(name="Ball", description="Soft, bouncy ball. Red in colour.")
# item2 = Item(name="Cube", description="Hard, square looking thing. Black in colour.")
# session.add(item1)
# session.add(item2)


# # commit the items to table
# session.commit()

# session.query(User).all()
# session.query(User).first()
# session.query(User).get(1)
# session.query(User.username).order_by(User.username).all()
# session.query(Item.description).filter(Item.name == "Cube").all()
# session.query(Item.id, Item.description).filter(Item.name == "Cube", Item.start_time < datetime.utcnow()).all()

Base.metadata.create_all(engine)