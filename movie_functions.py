from urllib import request, parse
from operator import attrgetter
import json
import re

from database.database_connection import connection
from models.movie import Movie

API_KEY = 'ee1034'
API_URL = 'http://www.omdbapi.com/?'
DATABASE = 'database/movies.sqlite'


def sort_movies(args):
    """Get all movies and sort them by the given attribute(s)."""
    cnx = connection(DATABASE)
    c = cnx.cursor()
    movies = Movie.load_all(c)
    none_to_zero(movies)
    none_to_empty_string(movies)
    runtime_convert_to_integer(movies)
    sorted_list = sorted(movies, key=attrgetter(*args.column),
                         reverse=args.order)
    columns = args.column
    result = prepare_result(columns, sorted_list)
    print_results(columns, result)
    c.close()
    cnx.close()


def filter_by_parameter(args):
    """Get a list of movies filter by the given parameter."""
    cnx = connection(DATABASE)
    c = cnx.cursor()
    if args.parameter == 'actor':
        filter_by = '[CAST]'  # db issue
        args.parameter = 'cast'
    else:
        filter_by = args.parameter
    value = replace_underscores(args.value)
    movies = Movie.load_with_filter(c, filter_by, value)
    result = prepare_result([args.parameter], movies)
    print_results([args.parameter], result)
    c.close()
    cnx.close()


def filter_by_movie_info(args):
    """Get a list of movies that match the given condition."""
    cnx = connection(DATABASE)
    c = cnx.cursor()
    movies = Movie.load_all(c)
    create_awards_dict(movies, overwrite_awards=True)
    if args.movie_info == 'oscar_nominated_no_win':
        result = [(i.title, i.awards['oscar_nominated']) for i in movies if
                  i.awards['oscar'] == 0 and i.awards['oscar_nominated'] > 0]
        columns = ['oscar nominated']
    elif args.movie_info == 'high_awards_win_rate':
        result = [(i.title, i.awards['awards'], i.awards['nominations'])
                  for i in movies if
                  i.awards['awards'] > i.awards['nominations'] * 0.8]
        columns = ['awards', 'nominations']
    else:
        result = [(i.title, i.box_office) for i in movies if i.box_office is not None and
                  i.box_office > 100_000_000]
        columns = ['box_office']
    print_results(columns, result)
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
        if attribute == 'runtime':
            runtime_convert_to_integer(movies_to_compare, set_zero=False)
        elif attribute == 'awards_won':
            attribute = 'awards'
            create_awards_dict(movies_to_compare, overwrite_awards=True)
            for movie in movies_to_compare:
                movie.awards = movie.awards['awards']
        movie = None
        try:
            movie = max(movies_to_compare, key=attrgetter(attribute))
        except TypeError:
            print('No necessary data for at least one of the movies')
        if movie:
            result = prepare_result([attribute], [movie])
            print_results([attribute], result)
    c.close()
    cnx.close()


def add_new_movie(args):
    """Add new movie to the database."""
    title = replace_underscores(args.movie_title)
    movie = Movie()
    movie.title = title
    response = get_data_from_api(movie, API_URL, API_KEY)
    if response:
        cnx = connection(DATABASE)
        c = cnx.cursor()
        check_database = Movie.load_by_title(c, movie.title)
        if check_database is None:
            m = movie.save(c)
            if m:
                print(f'Movie: {movie.title} successfully saved to the database')
        else:
            print(f'Movie: {movie.title} already in the database')
        cnx.commit()
        c.close()
        cnx.close()
    else:
        print(f'Movie: {title} not found.')


def high_scores(args):
    """Show high scores for movies in database."""
    result = {}
    cnx = connection(DATABASE)
    c = cnx.cursor()
    movies = Movie.load_all(c)
    runtime_convert_to_integer(movies)
    box_office_none_to_zero(movies)
    result['Runtime'] = max(movies, key=attrgetter('runtime'))
    result['Box Office'] = max(movies, key=attrgetter('box_office'))
    result['IMDB Rating'] = max(movies, key=(attrgetter('imdb_rating')))
    awards_dict = create_awards_dict(movies)
    oscars = key_with_max_value(awards_dict, 'oscar')
    nominations = key_with_max_value(awards_dict, 'nominations')
    awards_won = key_with_max_value(awards_dict, 'awards')
    print(oscars, nominations, awards_won, result['Runtime'].title,
          result['IMDB Rating'].title, result['Box Office'].title)
    c.close()
    cnx.close()


def replace_underscores(text):
    return text.replace('_', ' ')


def create_awards_dict(iterable, overwrite_awards=False):
    """Create dictionary with movie titles and awards info."""
    result = {}
    regex = {'oscar': r'won (\d+) oscar', 'awards': r'(\d+) wins',
             'oscar_nominated': r'nominated for (\d+) oscar',
             'nominations': r'(\d+) nomination'}
    for movie in iterable:
        award_dict = {'oscar': 0, 'oscar_nominated': 0, 'awards': 0,
                      'nominations': 0}
        if movie.awards is not None:
            for key in award_dict.keys():
                awards_number = re.search(regex[key], movie.awards, re.I)
                if awards_number is not None:
                    award_dict[key] = int(awards_number.group(1))
        if not overwrite_awards:
            result[movie.title] = award_dict
        else:
            movie.awards = award_dict
    return result


def key_with_max_value(dictionary, key):
    """Return the key with the max value."""
    v = [i[key] for i in list(dictionary.values())]
    k = list(dictionary.keys())
    max_value = max(v)
    return k[v.index(max_value)], max_value


def runtime_convert_to_integer(iterable, set_zero=True):
    """Convert movies runtime attribute from string to integer."""
    for movie in iterable:
        try:
            runtime = getattr(movie, 'runtime')
            setattr(movie, 'runtime', int(runtime.split(' ')[0]))
        except AttributeError:
            if set_zero:
                setattr(movie, 'runtime', 0)
            else:
                pass


def none_to_zero(iterable):
    """Replace None type objects to zero."""
    attributes = ['year', 'imdb_rating', 'imdb_votes', 'box_office']
    for attribute in attributes:
        for movie in iterable:
            if getattr(movie, attribute) is None:
                setattr(movie, attribute, 0)


def none_to_empty_string(iterable):
    """Replace None type objects to empty string."""
    attributes = ['genre', 'director', 'cast', 'writer', 'language',
                  'country', 'awards']
    for attribute in attributes:
        for movie in iterable:
            if getattr(movie, attribute) is None:
                setattr(movie, attribute, '')


def box_office_none_to_zero(iterable):
    """Change values of box office from None to 0."""
    for movie in iterable:
        if movie.box_office is None:
            movie.box_office = 0


def prepare_result(columns, movie_list):
    """Prepare a list of results to print."""
    result = []
    for movie in movie_list:
        data = [movie.title]
        for column in columns:
            data.append(getattr(movie, column))
        result.append(data)
    return result


def print_results(columns, result):
    """Format and print the results."""
    template = '{0:40}'
    for i in range(0, len(columns)):
        template += '| {%s:<10} ' % str(i + 1)
    print(template.format('Title', *columns))
    for raw in result:
        print(template.format(*raw))


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
        return True
    else:
        return False


def convert_to_int(value):
    """Remove non digit characters and convert string to integer."""
    return int(re.sub(r'\D', '', value))
