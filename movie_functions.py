from urllib import request, parse
import json
import re

from database.database_connection import connection
from models.movie import Movie
from operator import attrgetter

API_KEY = 'ee1034'
API_URL = 'http://www.omdbapi.com/?'
DATABASE = 'database/movies.sqlite'


def sort_movies(args):
    cnx = connection(DATABASE)
    c = cnx.cursor()
    movies = Movie.load_all(c, args.order, *args.column)
    for movie in movies:
        print(*[getattr(movie, i) for i in args.column])
    c.close()
    cnx.close()


def filter_by_parameter(args):
    cnx = connection(DATABASE)
    c = cnx.cursor()
    if args.parameter == 'actor':
        filter_by = '[CAST]'
    else:
        filter_by = args.parameter
    value = args.value.replace('_', ' ')
    movies = Movie.load_with_filter(c, filter_by, value)
    for movie in movies:
        print(movie.title, getattr(movie, 'cast'))
    c.close()
    cnx.close()


def filter_by_movie_info(args):
    cnx = connection(DATABASE)
    c = cnx.cursor()
    movies = Movie.load_all(c)
    if args.movie_info == 'oscar_nominated_no_win':
        pass
    elif args.movie_info == 'high_awards_win_rate':
        pass
    elif args.movie_info == 'high_box_office':
        result = [i for i in movies if i.box_office is not None and
                  i.box_office > 100_000_000]
        for movie in result:
            print(movie.title, movie.box_office)
    c.close()
    cnx.close()


def compare_movies(args):
    cnx = connection(DATABASE)
    c = cnx.cursor()
    movies_to_compare = []
    attribute = args.column
    for title in args.movie_title:
        movie = Movie.load_by_title(c, title.replace('_', ' '))
        if movie is not None:
            movies_to_compare.append(movie)
        else:
            print(f'Movie not found: {title}')
    if len(movies_to_compare) == 2:
        if attribute == 'runtime':
            runtime_convert_to_integer(movies_to_compare)
        elif attribute == 'awards_won':
            attribute = 'awards'  # TODO: convertion of awards in objects
        try:
            m = max(movies_to_compare, key=attrgetter(attribute))
            print(m.title, getattr(m, attribute))
        except TypeError:
            print('No necessary data for at least one of the movies')
    # print(movies_to_compare[0].runtime, movies_to_compare[1].runtime)
    c.close()
    cnx.close()


def runtime_convert_to_integer(iterable):
    for movie in iterable:
        runtime = getattr(movie, 'runtime')
        setattr(movie, 'runtime', int(runtime.split(' ')[0]))


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


def convert_to_int(value):
    """Remove non digit characters and convert to integer."""
    return int(re.sub(r'\D', '', value))
