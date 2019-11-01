from database.database_connection import connection
from models.movie import Movie
from operator import attrgetter

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


def compare(args):
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
