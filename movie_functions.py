from models.movie import Movie
from database.database_connection import connection

DATABASE = 'database/movies.sqlite'


def sort_movies(sort_by):
    cnx = connection(DATABASE)
    c = cnx.cursor()
    movies = Movie.load_all(c, sort_by.order, *sort_by.column)
    for movie in movies:
        print(movie.title, movie.year, movie.box_office)
    c.close()
    cnx.close()
