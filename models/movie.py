class Movie:
    """Represents a single movie."""

    def __init__(self):
        self.__id = -1
        self.title = None
        self.year = None
        self.runtime = None
        self.genre = None
        self.director = None
        self.cast = None
        self.writer = None
        self.language = None
        self.country = None
        self.awards = None
        self.imdb_rating = None
        self.imdb_votes = None
        self.box_office = None

    @property
    def id(self):
        return self.__id

    @staticmethod
    def load_by_title(cursor, title):
        """Load a movie with the given title."""
        sql = """SELECT * from MOVIES where title=?"""
        cursor.execute(sql, (title,))
        data = cursor.fetchone()
        if data:
            loaded_movie = Movie()
            loaded_movie.__id = data[0]
            loaded_movie.title = data[1]
            loaded_movie.year = data[2]
            loaded_movie.runtime = data[3]
            loaded_movie.genre = data[4]
            loaded_movie.director = data[5]
            loaded_movie.cast = data[6]
            loaded_movie.writer = data[7]
            loaded_movie.language = data[8]
            loaded_movie.country = data[9]
            loaded_movie.awards = data[10]
            loaded_movie.imdb_rating = data[11]
            loaded_movie.imdb_votes = data[12]
            loaded_movie.box_office = data[13]
            return loaded_movie
        else:
            return None

    def update(self, cursor):
        """Update information about the movie."""
        sql = """UPDATE MOVIES SET title=?, year=?, runtime=?, genre=?,
        director=?, cast=?, writer=?, language=?, country=?, awards=?,
        imdb_rating=?, imdb_votes=?, box_office=? WHERE id=?"""
        values = (self.title, self.year, self.runtime, self.genre,
                  self.director, self.cast, self.writer, self.language,
                  self.country, self.awards, self.imdb_rating,
                  self.imdb_votes, self.box_office, self.id)
        cursor.execute(sql, values)
        return True
