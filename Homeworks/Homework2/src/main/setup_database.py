# Create a new database named "films_db".
# Use the SQLAlchemy library to create the database and tables in Python.
# Part 1: Setting up the Database
# Create one table for films, with the following columns:
#     films table:
#         id (integer, primary key)
#         title (string)
#         director (string)
#         release year (integer)
# Part 2: Manipulating with Database
#     Create script that:
#         Add 3 film to the film table.
#         Update 1 film
#         Print data from table
#         Delete all data from table

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///films_db.db')

Base = declarative_base()

class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    director = Column(String)
    release_year = Column(Integer)

Base.metadata.create_all(engine)
