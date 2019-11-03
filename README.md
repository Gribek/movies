### Movies
 
Database file in this repository has already been populated. To test the script that fills initial data source with data from OMDb API replace sqlite files (database/movies.sqlite) and use fill_database.py.


#### Available commands

1. _sort_ command - sorting movies by chosen column(s).

Command pattern: sort column

where _column_ is one from the list: year, runtime, genre, director, cast, writer, language, country, awards, imdb_rating, imdb_votes, box_office. You can choose more than one column to sort by multiple columns, in that case just add its name at the end of command after space.
 
 To sort in the descending order add flag [-d]
 
 Example input:
 python movies.py sort year
 python movies,py sort year, imdb_rating
 
 
 2. _filter_by_ command - filter movies by chosen parameter