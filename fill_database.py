from database.database_connection import connection
from models.movie import Movie
from movie_functions import API_KEY, API_URL, DATABASE, get_data_from_api

# connecting to database
cnx = connection(DATABASE)
cursor = cnx.cursor()

# loading all movies from db
movies = Movie.load_all(cursor)

# getting information about each movie
for movie in movies:
    get_data_from_api(movie, API_URL, API_KEY)

    # updating information about the movie in db
    movie.update(cursor)

cnx.commit()
cursor.close()
cnx.close()
