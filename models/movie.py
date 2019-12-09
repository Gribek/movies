import re


class Movie:
    """Represents a single movie."""

    def __init__(self):
        self.__id = -1
        self.title = None
        self.year = None
        self.runtime = None
        self.genre = None
        self.director = None
        self.actors = None
        self.writer = None
        self.language = None
        self.country = None
        self.oscars_won = None
        self.oscar_nominations = None
        self.awards_won = None
        self.award_nominations = None
        self.imdb_rating = None
        self.imdb_votes = None
        self.box_office = None
        self.imdb_id = None

    @property
    def id(self):
        return self.__id

    @staticmethod
    def load_all(cursor):
        """Load all movies and sort them (optional)."""
        sql = 'SELECT * FROM MOVIES'
        movies = []
        cursor.execute(sql)
        for raw in cursor.fetchall():
            movie = Movie.create_object_from_data(raw)
            movies.append(movie)
        return movies

    @staticmethod
    def load_by_title(cursor, title):
        """Load a movie with the given title."""
        sql = """SELECT * from MOVIES where title like ?"""
        cursor.execute(sql, (title,))
        data = cursor.fetchone()
        if data:
            return Movie.create_object_from_data(data)
        else:
            return None

    @staticmethod
    def load_with_filter(cursor, filter_by, value):
        """Load movies filter by given parameter."""
        sql = """SELECT * FROM MOVIES where {} like ?""".format(filter_by)
        cursor.execute(sql, (f'%{value}%',))
        movies = []
        for raw in cursor.fetchall():
            movie = Movie.create_object_from_data(raw)
            movies.append(movie)
        return movies

    @staticmethod
    def create_object_from_data(data):
        """Create new object from the given data."""
        movie = Movie()
        movie.__id = data[0]
        movie.title = data[1]
        movie.year = data[2]
        movie.runtime = data[3]
        movie.genre = data[4]
        movie.director = data[5]
        movie.actors = data[6]
        movie.writer = data[7]
        movie.language = data[8]
        movie.country = data[9]
        movie.oscars_won = data[10]
        movie.oscar_nominations = data[11]
        movie.awards_won = data[12]
        movie.award_nominations = data[13]
        movie.imdb_rating = data[14]
        movie.imdb_votes = data[15]
        movie.box_office = data[16]
        movie.imdb_id = data[17]
        return movie

    @staticmethod
    def create_object_from_omdb_data(omdb_response):
        """Create new object from the data received from OMDb API."""
        movie = Movie()
        movie.title = omdb_response.movie_data['Title']
        movie.genre = omdb_response.movie_data['Genre']
        movie.director = omdb_response.movie_data['Director']
        movie.actors = omdb_response.movie_data['Actors']
        movie.writer = omdb_response.movie_data['Writer']
        movie.language = omdb_response.movie_data['Language']
        movie.country = omdb_response.movie_data['Country']
        movie.awards = omdb_response.movie_data['Awards']
        movie.imdb_id = omdb_response.movie_data['imdbID']

        movie.runtime = convert_to_int(omdb_response.movie_data['Runtime'])
        movie.year = convert_to_int(omdb_response.movie_data['Year'])
        movie.imdb_votes = convert_to_int(
            omdb_response.movie_data['imdbVotes'])
        movie.box_office = convert_to_int(
            omdb_response.movie_data['BoxOffice'])
        movie.imdb_rating = convert_to_float(
            omdb_response.movie_data['imdbRating'])

        awards = omdb_response.movie_data['Awards']
        regex = {'oscars_won': r'won (\d+) oscar', 'awards_won': r'(\d+) wins',
                 'oscar_nominations': r'nominated for (\d+) oscar',
                 'award_nominations': r'(\d+) nomination'}
        for key in regex:
            result = re.search(regex[key], awards, re.I)
            if result is not None:
                number = int(result.group(1))
            else:
                number = 0
            setattr(movie, key, number)
        return movie

    def save(self, cursor):
        """Save new movie object."""
        sql = """INSERT INTO MOVIES(title, year, runtime, genre, director,
        actors, writer, language, country, oscars_won, oscar_nominations,
        awards_won, award_nominations, imdb_rating, imdb_votes, box_office,
        imdb_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (self.title, self.year, self.runtime, self.genre,
                  self.director, self.actors, self.writer, self.language,
                  self.country, self.oscars_won, self.oscar_nominations,
                  self.awards_won, self.award_nominations, self.imdb_rating,
                  self.imdb_votes, self.box_office, self.imdb_id)
        cursor.execute(sql, values)
        return True

    def update(self, cursor):
        """Update information about the movie."""
        sql = """UPDATE MOVIES SET title=?, year=?, runtime=?, genre=?,
        director=?, actors=?, writer=?, language=?, country=?, oscars_won=?,
        oscar_nominations=?, awards_won=?, award_nominations=?, imdb_rating=?,
        imdb_votes=?, box_office=?, imdb_id=? WHERE id=?"""
        values = (self.title, self.year, self.runtime, self.genre,
                  self.director, self.actors, self.writer, self.language,
                  self.country, self.oscars_won, self.oscar_nominations,
                  self.awards_won, self.award_nominations, self.imdb_rating,
                  self.imdb_votes, self.box_office, self.imdb_id, self.id)
        cursor.execute(sql, values)
        return True


def convert_to_float(value):
    """Convert string to float."""
    try:
        return float(value)
    except TypeError:
        return None
    except ValueError:
        return None


def convert_to_int(value):
    """Remove non digit characters and convert string to integer."""
    try:
        return int(re.sub(r'\D', '', value))
    except TypeError:
        return None
    except ValueError:
        return None
