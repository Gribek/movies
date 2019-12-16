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
    attribute = args.column
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
    title = replace_underscores(args.movie_title)
    try:
        omdb = OmdbApiResponse(API_KEY, title)
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
                    print(f'Movie: {movie.title} successfully saved to the'
                          f' database')
            else:
                print(f'Movie: {omdb.movie_data["Title"]} already in the '
                      f'database')
            cnx.commit()
            c.close()
            cnx.close()
        else:
            print(f'Movie: {title} not found.')


def high_scores(args):
    """Show high scores for movies in database."""
    cnx = connection(DATABASE)
    c = cnx.cursor()
    movie_runtime = Movie.load_movie_with_max_attribute(c, 'runtime')
    movie_box_office = Movie.load_movie_with_max_attribute(c, 'box_office')
    movie_awards_won = Movie.load_movie_with_max_attribute(c, 'awards_won')
    movie_award_nominations = Movie.load_movie_with_max_attribute(
        c, 'award_nominations')
    movie_oscars_won = Movie.load_movie_with_max_attribute(c, 'oscars_won')
    movie_imdb_rating = Movie.load_movie_with_max_attribute(c, 'imdb_rating')
    data = [
        ('Runtime (min)', movie_runtime.title, movie_runtime.runtime),
        ('Box Office', movie_box_office.title, movie_box_office.box_office),
        ('Awards Won', movie_awards_won.title, movie_awards_won.title),
        ('Award Nominations', movie_award_nominations.title,
         movie_award_nominations.award_nominations),
        ('Oscars', movie_oscars_won.title, movie_oscars_won.oscars_won),
        ('IMDB Rating', movie_imdb_rating.title, movie_imdb_rating.imdb_rating)
    ]
    result = Result(columns=[], movie_list=[])
    result.columns = ['Movie', 'Value']
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

    omdb_url = 'http://www.omdbapi.com/?'

    def __init__(self, api_key, title):
        url = self.omdb_url + parse.urlencode({'apikey': api_key, 't': title})
        omdb_data = request.urlopen(url).read()
        json_data = json.loads(omdb_data)
        self.response = strtobool(json_data['Response'])
        self.movie_data = {
            'Title': None, 'Year': None, 'Runtime': None, 'Genre': None,
            'Director': None, 'Actors': None, 'Writer': None, 'Language': None,
            'Country': None, 'Awards': None, 'imdbRating': None,
            'imdbVotes': None, 'BoxOffice': None, 'imdbID': None
        }
        if self.response:
            for key in self.movie_data:
                try:
                    if json_data[key] != "N/A":
                        self.movie_data[key] = json_data[key]
                except KeyError:
                    pass
