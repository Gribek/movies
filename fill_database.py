from urllib import request, parse
import json
import re

from database.database_connection import connection
from models.movie import Movie
from movie_functions import API_KEY, API_URL, DATABASE


def convert_to_int(value):
    """Remove non digit characters and convert to integer."""
    return int(re.sub(r'\D', '', value))


def get_data_from_api(movie_obj, api_url, api_key):
    """Get data from api and save them in the movie object."""
    url = api_url + parse.urlencode({'apikey': api_key, 't': movie_obj.title})
    api_data = request.urlopen(url).read()
    json_data = json.loads(api_data)
    data_to_collect = {
        'Title': None, 'Year': None, 'Runtime': None, 'Genre': None,
        'Director': None, 'Actors': None, 'Writer': None, 'Language': None,
        'Country': None, 'Awards': None, 'imdbRating': None,
        'imdbVotes': None, 'BoxOffice': None
    }
    # getting information about movie from json
    if json_data['Response'] == 'True':
        for key in data_to_collect.keys():
            try:
                if json_data[key] != "N/A":
                    data_to_collect[key] = json_data[key]
            except KeyError:
                pass
        # editing movie object with collected data
        movie_obj.title = data_to_collect['Title']
        movie_obj.runtime = data_to_collect['Runtime']
        movie_obj.genre = data_to_collect['Genre']
        movie_obj.director = data_to_collect['Director']
        movie_obj.cast = data_to_collect['Actors']
        movie_obj.writer = data_to_collect['Writer']
        movie_obj.language = data_to_collect['Language']
        movie_obj.country = data_to_collect['Country']
        movie_obj.awards = data_to_collect['Awards']
        try:
            movie_obj.year = convert_to_int(data_to_collect['Year'])
        except TypeError:
            pass
        try:
            movie_obj.imdb_rating = float(data_to_collect['imdbRating'])
        except TypeError:
            pass
        try:
            movie_obj.imdb_votes = convert_to_int(data_to_collect['imdbVotes'])
        except TypeError:
            pass
        try:
            movie_obj.box_office = convert_to_int(data_to_collect['BoxOffice'])
        except TypeError:
            pass
    else:
        print(f'Movie: {movie_obj.title} not found.')


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
