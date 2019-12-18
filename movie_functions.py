from distutils.util import strtobool
from urllib.error import URLError
from urllib import request, parse
from operator import attrgetter
import json

from database.database_connection import connection
from models.movie import Movie
from settings import API_KEY, DATABASE


def sort_movies(args):
    """Get all movies and sort them by the given attribute(s)."""
    cnx = connection(DATABASE)
    c = cnx.cursor()
    movies = Movie.load_all(c, args.order, *args.column)
    result = Result(args.column, movies)
    result.display()
    c.close()
    cnx.close()


def filter_by_parameter(args):
    """Get a list of movies filter by the given parameter."""
    cnx = connection(DATABASE)
    c = cnx.cursor()
    if args.parameter == 'actor':
        args.parameter += 's'
    value = replace_underscores(args.value)
    column = args.parameter
    movies = Movie.load_with_filter(c, column, value)
    result = Result([column], movies)
    result.display()
    c.close()
    cnx.close()


def filter_by_movie_info(args):
    """Get a list of movies that match the given condition."""
    cnx = connection(DATABASE)
    c = cnx.cursor()
    movies = Movie.load_all(c)
    if args.movie_info == 'oscar_nominated_no_win':
        movie_list = [i for i in movies if i.oscars_won == 0 and
                      i.oscar_nominations > 0]
        columns = ['oscar nominated']
    elif args.movie_info == 'high_awards_win_rate':
        movie_list = [i for i in movies
                      if i.awards_won > i.award_nominations * 0.8]
        columns = ['awards_won', 'award_nominations']
    else:
        movie_list = [i for i in movies if i.box_office is not None and
                      i.box_office > 100_000_000]
        columns = ['box_office']
    result = Result(columns, movie_list)
    result.display()
    c.close()
    cnx.close()


def compare_movies(args):
    """Compare two movies by the given attribute."""
    cnx = connection(DATABASE)
    c = cnx.cursor()
    movies_to_compare = []
    attribute = args.category
    for title in args.movie_title:
        movie = Movie.load_by_title(c, replace_underscores(title))
        if movie is not None:
            movies_to_compare.append(movie)
        else:
            print(f'Movie not found: {title}')
    if len(movies_to_compare) == 2:
        try:
            movie = max(movies_to_compare, key=attrgetter(attribute))
        except TypeError:
            print('No necessary data for at least one of the movies')
        else:
            result = Result([attribute], [movie])
            result.display()
    c.close()
    cnx.close()


def add_new_movie(args):
    """Add new movie to the database."""
    title_or_imdb_id = replace_underscores(args.movie_identifier)
    try:
        omdb = OmdbApiResponse(title_or_imdb_id, args.imdb_id)
    except URLError:
        print('Unable to receive data from OMDb API. '
              'Check your internet connection.')
    else:
        if omdb.response:
            cnx = connection(DATABASE)
            c = cnx.cursor()
            check_db = Movie.load_by_imdb_id(c, omdb.movie_data['imdbID'])
            if check_db is None:
                movie = Movie.create_object_from_omdb_data(omdb.movie_data)
                m = movie.save(c)
                if m:
                    print(f'Movie: {movie.title} has been successfully saved '
                          f'to the database')
            else:
                print(f'Movie: {omdb.movie_data["Title"]} already in the '
                      f'database')
            cnx.commit()
            c.close()
            cnx.close()
        else:
            print(f'Movie: {title_or_imdb_id} not found.')


def high_scores(args):
    """Show high scores for movies in database."""
    cnx = connection(DATABASE)
    c = cnx.cursor()
    categories = ['runtime', 'box_office', 'awards_won', 'award_nominations',
                  'oscars_won', 'imdb_rating']
    first_column_data = ['Runtime (min)', 'Box Office ($)', 'Awards Won',
                         'Award Nominations', 'Oscars', 'IMDB Rating']
    data = []
    for i in range(len(categories)):
        top_movie = Movie.load_movie_with_max_attribute(c, categories[i])
        row_data = [first_column_data[i], top_movie.title,
                    getattr(top_movie, categories[i])]
        data.append(tuple(row_data))
    result = Result(columns=['Movie', 'Value'], movie_list=[])
    result.data = data
    result.display(first_col='CATEGORY', column_wide=25)
    c.close()
    cnx.close()


def replace_underscores(text):
    """Replace underscores with spaces."""
    return text.replace('_', ' ')


class Result:
    """The class that represents results displayed in terminal."""

    def __init__(self, columns, movie_list):
        self.columns = columns
        self.data = []
        for movie in movie_list:
            row = [movie.title]
            for column in columns:
                row.append(getattr(movie, column))
            self.data.append(row)

    def display(self, first_col='TITLE', column_wide=10):
        """Format and print the result."""
        c = [replace_underscores(x.upper()) for x in self.columns]
        template = '{0:40}'
        for i in range(0, len(c)):
            template += '| {%s:<%s} ' % (str(i + 1), str(column_wide))
        print(template.format(first_col, *c))
        for row in self.data:
            row_data = ['' if i is None else i for i in row]
            print(template.format(*row_data))


class OmdbApiResponse:
    """The class that represents the response from OMDb API.

    It sends a request to OMDb API and collects response data about
    selected movie.
    """

    __api_key = API_KEY
    __omdb_url = 'http://www.omdbapi.com/?'
    movie_data = {
        'Title': None, 'Year': None, 'Runtime': None, 'Genre': None,
        'Director': None, 'Actors': None, 'Writer': None, 'Language': None,
        'Country': None, 'Awards': None, 'imdbRating': None, 'imdbVotes': None,
        'BoxOffice': None, 'imdbID': None
    }

    def __init__(self, movie_identifier, is_imdb_id):
        request_data = {'apikey': self.__api_key}
        if is_imdb_id:
            request_data['i'] = movie_identifier
        else:
            request_data['t'] = movie_identifier
        url = self.__omdb_url + parse.urlencode(request_data)
        omdb_data = request.urlopen(url).read()
        json_data = json.loads(omdb_data)
        self.response = strtobool(json_data['Response'])
        if self.response:
            for key in self.movie_data:
                try:
                    if json_data[key] != "N/A":
                        self.movie_data[key] = json_data[key]
                except KeyError:
                    pass
