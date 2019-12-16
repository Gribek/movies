# import pytest  # TODO Fix tests
#
# from movie_functions import replace_underscores, create_awards_dict, \
#     key_with_max_value, runtime_convert_to_integer, none_to_zero, \
#     none_to_empty_string, box_office_none_to_zero, prepare_result, \
#     convert_to_int, print_results
# from models.movie import Movie
#
#
# @pytest.fixture
# def movie_list():
#     movie_list = [Movie() for i in range(0, 4)]
#     movie_list[0].title = 'Title 1'
#     movie_list[1].title = 'Title 2'
#     movie_list[2].title = 'Title 3'
#     movie_list[3].title = 'Title 4'
#     movie_list[0].awards = 'Won 2 Oscars. Another 79 wins & 59 nominations.'
#     movie_list[1].awards = 'Nominated for 2 Oscars. Another 11 wins & 16 nominations.'
#     movie_list[2].awards = '7 wins & 27 nominations.'
#     movie_list[0].runtime = '123 min'
#     attr = ['genre', 'director', 'cast', 'writer', 'language', 'country',
#             'awards', 'year', 'imdb_rating', 'imdb_votes', 'box_office']
#     for i in attr:
#         setattr(movie_list[3], i, None)
#     return movie_list
#
#
# @pytest.fixture
# def columns():
#     return ['runtime', 'imdb_rating']
#
#
# @pytest.fixture
# def result():
#     return [['Inception', 111, 8.8], ['Die Hard', 144, 7.6]]
#
#
# def test_replace_underscores():
#     assert replace_underscores('Toy_story') == 'Toy story'
#     assert replace_underscores('Avatar') == 'Avatar'
#
#
# def test_create_awards_dict_overwrite_false(movie_list):
#     assert create_awards_dict(movie_list)['Title 1'] == {
#         'oscar': 2, 'awards': 79, 'oscar_nominated': 0, 'nominations': 59}
#     assert create_awards_dict(movie_list, False)['Title 2'] == {
#         'oscar': 0, 'awards': 11, 'oscar_nominated': 2, 'nominations': 16}
#     assert create_awards_dict(movie_list)['Title 3'] == {
#         'oscar': 0, 'awards': 7, 'oscar_nominated': 0, 'nominations': 27}
#     assert create_awards_dict(movie_list, False)['Title 4'] == {
#         'oscar': 0, 'awards': 0, 'oscar_nominated': 0, 'nominations': 0}
#
#
# def test_create_awards_dict_overwrite_true(movie_list):
#     create_awards_dict(movie_list, True)
#     movie_1 = movie_list[0]
#     assert movie_1.awards['oscar'] == 2
#     assert movie_1.awards['oscar_nominated'] == 0
#     assert movie_1.awards['nominations'] == 59
#     assert movie_1.awards['awards'] == 79
#
#
# def test_key_with_max_value(movie_list):
#     awards_dict = create_awards_dict(movie_list)
#     assert key_with_max_value(awards_dict, 'oscar') == ('Title 1', 2)
#     assert key_with_max_value(awards_dict, 'oscar_nominated') == ('Title 2', 2)
#
#
# def test_runtime_convert_to_integer_set_zero_true(movie_list):
#     runtime_convert_to_integer(movie_list, True)
#     movie_1 = movie_list[0]
#     movie_2 = movie_list[3]
#     assert movie_1.runtime == 123
#     assert type(movie_1.runtime) is int
#     assert movie_2.runtime == 0
#
#
# def test_runtime_convert_to_integer_set_zero_false(movie_list):
#     runtime_convert_to_integer(movie_list, False)
#     movie_1 = movie_list[0]
#     movie_2 = movie_list[3]
#     assert movie_1.runtime == 123
#     assert type(movie_1.runtime) is int
#     assert movie_2.runtime is None
#
#
# def test_none_to_zero(movie_list):
#     none_to_zero(movie_list)
#     movie = movie_list[3]
#     assert movie.imdb_rating == 0
#     assert movie.imdb_votes == 0
#     assert movie.year == 0
#     assert movie.box_office == 0
#
#
# def test_none_to_empty_string(movie_list):
#     none_to_empty_string(movie_list)
#     movie = movie_list[3]
#     assert movie.genre == ''
#     assert movie.director == ''
#     assert movie.cast == ''
#     assert movie.writer == ''
#     assert movie.language == ''
#     assert movie.country == ''
#     assert movie.awards == ''
#
#
# def test_box_office_none_to_zero(movie_list):
#     box_office_none_to_zero(movie_list)
#     movie = movie_list[3]
#     assert movie.box_office == 0
#
#
# def test_prepare_result(movie_list, columns):
#     result = prepare_result(columns, movie_list)
#     movie_1 = movie_list[0]
#     movie_2 = movie_list[1]
#     movie_3 = movie_list[2]
#     movie_4 = movie_list[3]
#     assert result == [
#         [movie_1.title, movie_1.runtime, movie_1.year],
#         [movie_2.title, movie_2.runtime, movie_2.year],
#         [movie_3.title, movie_3.runtime, movie_3.year],
#         [movie_4.title, movie_4.runtime, movie_4.year]
#     ]
#
#
# def test_convert_to_int():
#     assert type(convert_to_int('dsa23e$')) is int
#     assert convert_to_int('fds1@2!3$d4sdf-  re5') == 12345
#     assert convert_to_int('123') == 123
#     assert convert_to_int('string') is None
#     assert convert_to_int(None) is None
#
#
# def test_if_print_results_prints_all_data(capfd, columns, result):
#     print_results(columns, result)
#     out, err = capfd.readouterr()
#     assert 'Inception' in out
#     assert 'Die Hard' in out
#     assert '111' in out
#     assert '144' in out
#     assert '8.8' in out
#     assert '7.6' in out
#
#
# def test_if_print_results_prints_headers_correctly(capfd, columns, result):
#     print_results(columns, result)
#     out, err = capfd.readouterr()
#     assert 'TITLE' in out
#     assert 'IMDB RATING' in out
#     assert 'RUNTIME' in out
