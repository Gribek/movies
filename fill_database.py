from urllib import request, parse
import json
import re

from database.database_connection import connection
from models.movie import Movie


def convert_to_int(value):
    """Remove non digit characters and convert to integer."""
    return int(re.sub(r'\D', '', value))


cnx = connection('database/movies.sqlite')
cursor = cnx.cursor()

# loading all movies from db
movies = Movie.load_all(cursor)

# getting information about each movie
for movie in movies:
    url = 'http://www.omdbapi.com/?' + parse.urlencode({'apikey': 'ee1034',
                                                        't': movie.title})
    api_data = request.urlopen(url).read()
    json_data = json.loads(api_data)
    data_to_collect = {
        'Title': None, 'Year': None, 'Runtime': None, 'Genre': None,
        'Director': None, 'Actors': None, 'Writer': None, 'Language': None,
        'Country': None, 'Awards': None, 'imdbRating': None,
        'imdbVotes': None, 'BoxOffice': None
    }
    if json_data['Response'] == 'True':
        for key in data_to_collect.keys():
            try:
                if json_data[key] != "N/A":
                    data_to_collect[key] = json_data[key]
            except KeyError:
                pass
        # editing movie object with collected data
        movie.title = data_to_collect['Title']
        movie.runtime = data_to_collect['Runtime']
        movie.genre = data_to_collect['Genre']
        movie.director = data_to_collect['Director']
        movie.cast = data_to_collect['Actors']
        movie.writer = data_to_collect['Writer']
        movie.language = data_to_collect['Language']
        movie.country = data_to_collect['Country']
        movie.awards = data_to_collect['Awards']
        try:
            movie.year = convert_to_int(data_to_collect['Year'])
        except TypeError:
            pass
        try:
            movie.imdb_rating = float(data_to_collect['imdbRating'])
        except TypeError:
            pass
        try:
            movie.imdb_votes = convert_to_int(data_to_collect['imdbVotes'])
        except TypeError:
            pass
        try:
            movie.box_office = convert_to_int(data_to_collect['BoxOffice'])
        except TypeError:
            pass
    else:
        print(f'Movie: {movie.title} not found.')

    # updating information about the movie in db
    movie.update(cursor)

cnx.commit()
cursor.close()
cnx.close()
