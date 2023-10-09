# Create a session to interact with the DB
from sqlalchemy.orm import sessionmaker

from Homeworks.Homework2.src.main.setup_database import engine, Film

Session = sessionmaker(bind=engine)
session = Session()

# Add 3 films
film1 = Film(title="Inception", director="Christopher Nolan", release_year=2010)
film2 = Film(title="Interstellar", director="Christopher Nolan", release_year=2014)
film3 = Film(title="The Matrix", director="The Wachowskis", release_year=1999)

session.add(film1)
session.add(film2)
session.add(film3)
session.commit()

# Update 1 film
film_to_update = session.query(Film).filter_by(title="Inception").first()
film_to_update.release_year = 2011
session.commit()

# Print data
films = session.query(Film).all()
for film in films:
    print(film.id, film.title, film.director, film.release_year)

# Delete all data
session.query(Film).delete()
session.commit()

# Print data again to confirm deletion
films = session.query(Film).all()
print("After deletion:")
for film in films:
    print(film.id, film.title, film.director, film.release_year)
