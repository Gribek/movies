class Movie:
    """Represents a single movie entry."""

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

    def update(self, cursor):
        sql = """UPDATE MOVIES SET title=?, year=?, runtime=?, genre=?,
        director=?, cast=?, writer=?, language=?, country=?, awards=?,
        imdb_rating=?, imdb_votes=?, box_office=? WHERE id=?"""
        values = (self.title, self.year, self.runtime, self.genre,
                  self.director, self.cast, self.writer, self.language,
                  self.country, self.awards, self.imdb_rating,
                  self.imdb_votes, self.box_office, self.id)
        cursor.execute(sql, values)
        return True
