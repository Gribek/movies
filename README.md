### Movies
 
Database file in this repository has already been populated. To test the script that fills initial data source with data from OMDb API replace sqlite files (database/movies.sqlite) and use fill_database.py.


#### Available commands

1. _sort_ command - sorting movies by chosen column(s).

Command pattern: movies.py sort column

where _column_ is one from the list: year, runtime, genre, director, cast, writer, language, country, awards, imdb_rating, imdb_votes, box_office. You can choose more than one column to sort by multiple columns, in that case just add its name at the end of the command after space.

To sort in the descending order add flag: -d
 
 Example input:  
 python movies.py sort year  
 python movies.py sort year imdb_rating
 
 
 2. _filter_by_ command - filter movies by chosen parameter
 
 To filter by actor, director or language use following command pattern:  
 movies.py filter_by parameter parameter_name value  
 
 where _parameter_ is a subcommand,  
 _parameter_name_ is one option from list: actor, director, language  
 _value_ is phrase that you looking for. You can search by actor/director surname only or by name and surname. In the second case use underscore instead of space and type name first, i.e. _name___surname_. _value_ is case insensitive.
 
 Example input:  
 python movies.py filter_by parameter actor Bruce_Willis  
 python movies.py filter_by parameter language russian

 To filter by information about awards and box office use following command pattern:  
 movie.py filter_by movie movie_info
 
 where _movie_ is a subcommand
 _movie_info_ is one option from list: oscar_nominated_no_win, high_awards_win_rate, high_box_office  
 _oscar_nominated_no_win_ - shows movies that was nominated for an Oscar but did not win any  
 _high_awards_win_rate - shows movies that won more than 80% of nominations  
 _high_box_office_ - shows movies that earned more than 100,000,000 $
 
 Example input:  
 python movies.py filter_by movie high_box_office
 
 
 3. _compare_ command - compare two movies by selected column
 
 Command pattern: movies.py compare column movie_title movie_title
 
 where _column_ is one option from list: imdb_rating, box_office, awards_won, runtime  
 _movie_title_ is title of one of the movies you want to compare. If the name of the movie consist of more than one word, use underscores instead of spaces. _movie_title_ is case insensitive.  
 
  Example input:  
 python movies.py compare awards_won inception toy_story
 
 Take into consideration that the comparison is not always possible due to the lack of necessary data about the movie. In that case, you will be notified by an appropriate message.
 
 
 4. _add_ command - add new movie to the database
 
 Command pattern: movies.py add movie_title
 
 where _movie_title_ is a title of movie you want to add. If the name of the movie consist of more than one word, use underscores instead of spaces.
 
 Example input:  
 python movies.py add the_hangover
 
 If movie is already in the database, you will be informed.
 
 5. _highscores_ command - show current top values in following categories: runtime, bo office earnings, awards won, nominations, Oscars won, IMDB rating
 
  Command pattern: movies.py highscores
  
  Eample input:  
  python movies.py highscores
  
  This command does not require or accept any additional arguments.
  