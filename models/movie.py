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
