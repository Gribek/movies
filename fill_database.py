from urllib import request, parse
import json
import re

from database.database_connection import connection
from models.movie import Movie

cnx = connection('database/movies.sqlite')
cursor = cnx.cursor()

# loading all movies from db
movies = Movie.load_all(cursor)

# getting information about each movie
for movie in movies:
    url = 'http://www.omdbapi.com/?' + parse.urlencode({'apikey': 'ee1034',
                                                        't': movie.title})
    data = request.urlopen(url).read()
    json_data = json.loads(data)
    if json_data['Response'] == 'True':
        movie.title = json_data['Title']
        movie.year = int(re.sub(r'\D', '', json_data['Year']))
        movie.runtime = json_data['Runtime']
        movie.genre = json_data['Genre']
        movie.director = json_data['Director']
        movie.cast = json_data['Actors']
        movie.writer = json_data['Writer']
        movie.language = json_data['Language']
        movie.country = json_data['Country']
        movie.awards = json_data['Awards']
        movie.imdb_rating = float(json_data['imdbRating'])
        movie.imdb_votes = int(re.sub(r'\D', '', json_data['imdbVotes']))
        try:
            if json_data['BoxOffice'] != "N/A":
                movie.box_office = int(re.sub(r'\D', '', json_data['BoxOffice']))
        except KeyError:
            pass
    else:
        print(f'Movie: {movie.title} not found.')

    # updating information about the movie in db
    movie.update(cursor)
    cnx.commit()

cursor.close()
cnx.close()
