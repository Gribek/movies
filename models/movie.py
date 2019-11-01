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
    def load_all(cursor, desc=False, *sort):
        """Load all movies and sort them (optional)."""
        sql = 'SELECT * FROM MOVIES'
        if sort:
            if desc:
                order = 'desc'
            else:
                order = ''
            sql += ' ORDER BY '
            for column in sort[:-1]:
                sql += f'{column} {order}, '
            sql += f'{sort[-1]} {order}'
        movies = []
        cursor.execute(sql)
        for raw in cursor.fetchall():
            movie = Movie.create_object_from_data(raw)
            movies.append(movie)
        return movies

    @staticmethod
    def load_by_title(cursor, title):
        """Load a movie with the given title."""
        sql = """SELECT * from MOVIES where title=?"""
        cursor.execute(sql, (title,))
        data = cursor.fetchone()
        if data:
            return Movie.create_object_from_data(data)
        else:
            return None

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
        movie.cast = data[6]
        movie.writer = data[7]
        movie.language = data[8]
        movie.country = data[9]
        movie.awards = data[10]
        movie.imdb_rating = data[11]
        movie.imdb_votes = data[12]
        movie.box_office = data[13]
        return movie

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
