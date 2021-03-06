import argparse

from movie_functions import sort_movies, compare_movies, filter_by_parameter, \
    show_movies_with_condition, add_new_movie, high_scores, movie_details

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# sort command
parser_sort = subparsers.add_parser('sort')
parser_sort.add_argument('column', nargs='+', choices=[
    'year', 'runtime', 'genre', 'director', 'actors', 'writer', 'language',
    'country', 'awards_won', 'award_nominations', 'oscar_nominations',
    'oscars_won', 'imdb_rating', 'imdb_votes', 'box_office'])
parser_sort.add_argument('-d', '--order', action='store_true')
parser_sort.set_defaults(function=sort_movies)

# filter_by command
parser_filter_by = subparsers.add_parser('filter_by')
parser_filter_by.add_argument('parameter', choices=[
    'actor', 'director', 'language', 'year', 'genre', 'writer', 'country'])
parser_filter_by.add_argument('value')
parser_filter_by.set_defaults(function=filter_by_parameter)

# show_movies command
parser_show_movies = subparsers.add_parser('show_movies')
parser_show_movies.add_argument('condition', choices=[
    'oscar_nominated_no_win', 'high_awards_win_rate', 'high_box_office'])
parser_show_movies.set_defaults(function=show_movies_with_condition)

# compare command
parser_compare = subparsers.add_parser('compare')
parser_compare.add_argument(
    'category', choices=['imdb_rating', 'box_office', 'awards_won', 'runtime',
                         'award_nominations', 'oscar_nominations',
                         'oscars_won'])
parser_compare.add_argument('movie_title', nargs=2)
parser_compare.set_defaults(function=compare_movies)

# add command
parser_add = subparsers.add_parser('add')
parser_add.add_argument('movie_identifier')
parser_add.add_argument('-i', '--imdb_id', action='store_true')
parser_add.set_defaults(function=add_new_movie)

# highscores command
parser_highscores = subparsers.add_parser('highscores')
parser_highscores.set_defaults(function=high_scores)

# movie_details command
parser_movie_details = subparsers.add_parser('movie_details')
parser_movie_details.add_argument('movie_identifier')
parser_movie_details.add_argument('-i', '--imdb_id', action='store_true')
parser_movie_details.set_defaults(function=movie_details)

args = parser.parse_args()
args.function(args)
