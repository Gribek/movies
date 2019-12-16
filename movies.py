import argparse

from movie_functions import sort_movies, compare_movies, filter_by_parameter, \
    filter_by_movie_info, add_new_movie, high_scores

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
subparsers_filter_by = parser_filter_by.add_subparsers()

parser_filter_by_parameter = subparsers_filter_by.add_parser('parameter')
parser_filter_by_parameter.add_argument('parameter', choices=[
    'actor', 'director', 'language'])
parser_filter_by_parameter.add_argument('value')
parser_filter_by_parameter.set_defaults(function=filter_by_parameter)

parser_filter_by_movie_info = subparsers_filter_by.add_parser('movie')
parser_filter_by_movie_info.add_argument('movie_info', choices=[
    'oscar_nominated_no_win', 'high_awards_win_rate', 'high_box_office'])
parser_filter_by_movie_info.set_defaults(function=filter_by_movie_info)

# compare command
parser_compare = subparsers.add_parser('compare')
parser_compare.add_argument(
    'column', choices=['imdb_rating', 'box_office', 'awards_won', 'runtime'])
parser_compare.add_argument('movie_title', nargs=2)
parser_compare.set_defaults(function=compare_movies)

# add command
parser_add = subparsers.add_parser('add')
parser_add.add_argument('movie_title')
parser_add.set_defaults(function=add_new_movie)

# highscores command
parser_highscores = subparsers.add_parser('highscores')
parser_highscores.set_defaults(function=high_scores)

args = parser.parse_args()
args.function(args)
