import pytest

from movie_functions import replace_underscores, Result, OmdbApiResponse

from models.movie import Movie


@pytest.fixture
def movie_list():
    movie_list = [Movie() for i in range(0, 4)]
    movie_list[0].title = 'Title 1'
    movie_list[1].title = 'Title 2'
    movie_list[2].title = 'Title 3'
    movie_list[3].title = 'Title 4'
    movie_list[0].language = 'English'
    movie_list[1].language = 'English'
    movie_list[2].language = 'German, English, Spanish'
    movie_list[3].language = 'Polish'
    movie_list[0].imdb_rating = 5.1
    movie_list[1].imdb_rating = 8.5
    movie_list[2].imdb_rating = 7.3
    movie_list[3].imdb_rating = 6.2
    return movie_list


@pytest.fixture
def columns():
    return ['language', 'imdb_rating']


@pytest.fixture
def result_data():
    data = [
        ['Inception', 'English', 8.8], ['Die Hard', 'English, Spanish', 7.6],
        ['Movie with very long title', 'English, Spanish, German', 8.3]
    ]
    return data


@pytest.fixture()
def result_object(columns, result_data):
    result = Result(columns, [])
    result.data = result_data
    return result


def test_replace_underscores():
    assert replace_underscores('Toy_story') == 'Toy story'
    assert replace_underscores('Avatar') == 'Avatar'


def test_set_awards_attributes(movie_list):
    movie_1 = movie_list[0]
    Movie.set_awards_attributes(
        'Won 2 Oscars. Another 79 wins & 59 nominations.', movie_1)
    assert movie_1.oscars_won == 2
    assert movie_1.oscar_nominations == 0
    assert movie_1.awards_won == 79
    assert movie_1.award_nominations == 59
    movie_2 = movie_list[1]
    Movie.set_awards_attributes(
        'Nominated for 2 Oscars. Another 11 wins & 16 nominations.', movie_2)
    assert movie_2.oscars_won == 0
    assert movie_2.oscar_nominations == 2
    assert movie_2.awards_won == 11
    assert movie_2.award_nominations == 16
    movie_3 = movie_list[2]
    Movie.set_awards_attributes('7 wins & 27 nominations.', movie_3)
    assert movie_3.oscars_won == 0
    assert movie_3.oscar_nominations == 0
    assert movie_3.awards_won == 7
    assert movie_3.award_nominations == 27


def test_set_awards_attributes_no_awards_info(movie_list):
    movie = movie_list[0]
    Movie.set_awards_attributes(None, movie)
    assert movie.oscars_won == 0
    assert movie.oscar_nominations == 0
    assert movie.awards_won == 0
    assert movie.award_nominations == 0


def test_convert_to_int():
    assert Movie.convert_to_int('123') == 123
    assert Movie.convert_to_int('$12343355') == 12343355
    assert type(Movie.convert_to_int('123')) is int
    assert Movie.convert_to_int('-10dfd 0d') == 100
    assert Movie.convert_to_int(None) is None
    assert Movie.convert_to_int('abcdefg') is None
    assert Movie.convert_to_int('') is None


def test_convert_to_float():
    assert Movie.convert_to_float('8.2') == 8.2
    assert type(Movie.convert_to_float('8.4')) is float
    assert Movie.convert_to_float(None) is None
    assert Movie.convert_to_float('1.2abcdefg') is None
    assert Movie.convert_to_float('') is None


def test_create_object_from_data():
    data = (
        16, 'Iron Man', 2008, 126, 'Action, Adventure, Sci-Fi', 'Jon Favreau',
        'Robert Downey Jr., Terrence Howard, Jeff Bridges, Gwyneth Paltrow',
        'Mark Fergus (screenplay), Hawk Ostby (screenplay), Art Marcum (screen'
        'play), Matt Holloway (screenplay), Stan Lee (characters), Don Heck ('
        'characters), Larry Lieber (characters), Jack Kirby (characters)',
        'Hungarian, Kurdish, Hindi, English, Persian, Urdu, Arabic', 'USA', 0,
        2, 20, 65, 7.9, 889014, 318298180, 'tt0371746'
    )
    test_movie = Movie.create_object_from_data(data)
    assert test_movie._Movie__id == 16
    assert test_movie.title == 'Iron Man'
    assert test_movie.year == 2008
    assert test_movie.runtime == 126
    assert test_movie.genre == 'Action, Adventure, Sci-Fi'
    assert test_movie.director == 'Jon Favreau'
    assert test_movie.actors == 'Robert Downey Jr., Terrence Howard, Jeff ' \
                                'Bridges, Gwyneth Paltrow'
    assert test_movie.writer.startswith('Mark Fergus (screenplay)')
    assert test_movie.writer.endswith('Jack Kirby (characters)')
    assert test_movie.language == 'Hungarian, Kurdish, Hindi, English, ' \
                                  'Persian, Urdu, Arabic'
    assert test_movie.country == 'USA'
    assert test_movie.oscars_won == 0
    assert test_movie.oscar_nominations == 2
    assert test_movie.awards_won == 20
    assert test_movie.award_nominations == 65
    assert test_movie.imdb_rating == 7.9
    assert test_movie.imdb_votes == 889014
    assert test_movie.box_office == 318298180
    assert test_movie.imdb_id == 'tt0371746'


def test_create_object_from_omdb_data():
    omdb_data = {
        'Title': 'Iron Man 3', 'Year': '2013', 'Runtime': '130 min',
        'Genre': 'Action, Adventure, Sci-Fi', 'Director': 'Shane Black',
        'Actors': 'Robert Downey Jr., Gwyneth Paltrow, Don Cheadle,'
                  ' Guy Pearce',
        'Writer': 'Drew Pearce (screenplay by), Shane Black (screenplay by), '
                  'Stan Lee (based on the Marvel comic book by), Don Heck '
                  '(based on the Marvel comic book by), Larry Lieber (based on'
                  ' the Marvel comic book by), Jack Kirby (based on the Marvel'
                  ' comic book by), Warren Ellis (based on the "Extremis" '
                  'mini-series written by), Adi Granov (based on the '
                  '"Extremis" mini-series illustrated by)',
        'Language': 'English', 'Country': 'USA',
        'Awards': 'Nominated for 1 Oscar. Another 19 wins & 62 nominations.',
        'imdbRating': '7.2', 'imdbVotes': '716,950',
        'BoxOffice': '$408,992,272', 'imdbID': 'tt1300854'
    }

    test_movie = Movie.create_object_from_omdb_data(omdb_data)
    assert test_movie.title == 'Iron Man 3'
    assert test_movie.year == 2013
    assert test_movie.runtime == 130
    assert test_movie.genre == 'Action, Adventure, Sci-Fi'
    assert test_movie.director == 'Shane Black'
    assert test_movie.actors == 'Robert Downey Jr., Gwyneth Paltrow, ' \
                                'Don Cheadle, Guy Pearce'
    assert test_movie.writer.startswith('Drew Pearce (screenplay by)')
    assert test_movie.writer.endswith('mini-series illustrated by)')
    assert test_movie.language == 'English'
    assert test_movie.country == 'USA'
    assert test_movie.oscars_won == 0
    assert test_movie.oscar_nominations == 1
    assert test_movie.awards_won == 19
    assert test_movie.award_nominations == 62
    assert test_movie.imdb_rating == 7.2
    assert test_movie.imdb_votes == 716_950
    assert test_movie.box_office == 408_992_272
    assert test_movie.imdb_id == 'tt1300854'


def test_omdbapiresponse_init_with_imdb_id():
    api_response = OmdbApiResponse('tt1300854', is_imdb_id=True)
    assert hasattr(api_response, 'response')
    assert hasattr(api_response, 'movie_data')
    assert api_response.response
    assert api_response.movie_data['Title'] == 'Iron Man 3'
    assert api_response.movie_data['BoxOffice'] == '$408,992,272'


def test_omdbapiresponse_init_with_wrong_imdb_id():
    api_response = OmdbApiResponse('wrong imdb id', is_imdb_id=True)
    assert not api_response.response
    assert api_response.movie_data['Title'] is None
    assert api_response.movie_data['BoxOffice'] is None


def test_omdbapiresponse_init_with_movie_title():
    api_response_3 = OmdbApiResponse('Iron Man', is_imdb_id=False)
    assert api_response_3.response
    assert api_response_3.movie_data['Title'] == 'Iron Man'
    assert api_response_3.movie_data['Runtime'] == '126 min'


def test_result_init(columns, movie_list):
    result = Result(columns, movie_list)
    movie_1, movie_2, movie_3, movie_4 = movie_list
    assert hasattr(result, 'columns'), '"column" attribute is missing'
    assert hasattr(result, 'data'), '"data" attribute is missing'
    assert 'LANGUAGE'.upper() in result.columns, 'Column name is missing'
    assert 'IMDB RATING' in result.columns, 'Column name is missing'
    assert 'language' not in result.columns, 'Column name is not in uppercase'
    assert 'IMDB_RATING' not in result.columns, 'Column names with underscores'
    assert result.data == [
        [movie_1.title, movie_1.language, movie_1.imdb_rating],
        [movie_2.title, movie_2.language, movie_2.imdb_rating],
        [movie_3.title, movie_3.language, movie_3.imdb_rating],
        [movie_4.title, movie_4.language, movie_4.imdb_rating]
    ], 'Data incorrectly arranged in the list'


def test_result_display_column_headers(capsys, result_object):
    result_object.display()
    out = capsys.readouterr().out
    error_message = 'Name of the column is missing in output'
    assert 'TITLE' in out, error_message
    assert 'LANGUAGE' in out, error_message
    assert 'IMDB RATING' in out, error_message


def test_result_display_movie_data(capsys, result_object):
    result_object.display()
    out = capsys.readouterr().out
    title_error_message = 'Movie title is missing in output'
    data_error_message = 'Movie data is missing in output'
    assert 'Inception' in out, title_error_message
    assert 'Die Hard' in out, title_error_message
    assert 'English' in out, data_error_message
    assert 'Spanish' in out, data_error_message
    assert '8.8' in out, data_error_message
    assert '7.6' in out, data_error_message


def test_check_data_length_first_column(result_object):
    max_length_first_column = Result.check_data_length(result_object)
    assert max_length_first_column == len('Movie with very long title'), \
        'Width of the first column set incorrectly'


def test_check_data_length_further_columns(result_object):
    max_length_second_column = Result.check_data_length(result_object, 0)
    assert max_length_second_column == len('English, Spanish, German'), \
        'Width of the second column set incorrectly'


def test_check_data_length_short_numerical_values(result_object):
    min_value_check = Result.check_data_length(result_object, 1)
    error_message = 'Column width set incorrectly when the column title is ' \
                    'wider than the data values'
    assert min_value_check == len('imdb_rating'), error_message
