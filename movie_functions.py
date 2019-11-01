from database.database_connection import connection
from models.movie import Movie

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
