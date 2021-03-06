# Movies
### Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Available commands](#available-commands)

### General info
This is a command line program that allows you to create a personal database of information related to movies. The data source for the application is the OMDb API. 

### Technologies
* Python 3.7.5
* SQLite 3.22.0
* pytest 5.2.2

### Setup
To test this program, download the repository and try the commands below. The attached database file contains a certain amount of data, so you'll see the result of the commands you are running. 

If you want to use this program, generate your API key here: http://www.omdbapi.com/apikey.aspx and place new value in the settings.py file.  
Also in setting.py, change DATABASE value to 'movies_db.sqlite', which will let you to start with an empty database.

To complete the program setup, prepare a virtual environment for it and install all dependencies using the command:
```
$ pip install -r requirements.txt
```

### Available commands

Note that the application requires Python 3, so you may need to use the python3 command instead of python.

**1. _add_ command - add new movie to the database**
 
 Command pattern: movies.py add movie_identifier
 
 where:  
  _movie_identifier_ is a title or an imdb id of movie you want to add. If the title of the movie consist of more than one word, use underscores instead of spaces.
 
 Use flag: -i, to add movie using imdb id instead of movie title
 
 Example input:  
 ```
 $ python movies.py add the_godfather
 ```
 or
 ```
 $ python movies.py add tt0068646 -i
 ```
 
 If movie is already in the database, you will be informed.
 

**2. _movie_details_ commnad - show all information about a single movie**

 Command pattern: movies.py movie_details movie_identifier
 
 where:  
  _movie_identifier_ is a title or an imdb id of the movie you want to view information about. If the title of the movie consist of more than one word, use underscores instead of spaces.

 Use flag: -i, to show information about the movie using imdb id instead of movie title
 
 Example input:  
 ```
 $ python movies.py movie_details the_godfather
 ```
 or
 ```
 $ python movies.py movie_details tt0068646 -i
 ```
  

**3. _sort_ command - sorting movies by chosen column(s).**

Command pattern: movies.py sort column

where:  
 _column_ is one from the list: year, runtime, genre, director, cast, writer, language, country, awards, imdb_rating, imdb_votes, box_office. You can choose more than one column to sort by multiple columns, in that case just add its name at the end of the command after space.

 Use flag: -d, to sort in the descending order
 
 Example input:  
 ```
 $ python movies.py sort year  
 $ python movies.py sort year imdb_rating
 ```
 
 
 **4. _filter_by_ command - filter movies by chosen parameter**
 
 Command pattern: movies.py filter_by parameter value  
 
 where:  
 _parameter_ is an option from list: actor, country, director, genre, language, writer, year
 _value_ is phrase that you looking for. You can search by actor/director surname only or by name and surname. In the second case use underscore instead of space and type name first, i.e. _name_surname_. _value_ is case insensitive.
 
 Example input:  
 ```
 $ python movies.py filter_by actor Bruce_Willis  
 $ python movies.py filter_by language spanish
 ```


**5. _show_movies_ - show movies that match the given condition**
 
 Command pattern: movie.py show_movies condition
 
 where condition is one of the following:  
 _oscar_nominated_no_win_ - shows movies that have been nominated for an Oscar but have not won any  
 _high_awards_win_rate_ - shows movies that have won at least half of nominations  
 _high_box_office_ - shows movies that have earned more than 100,000,000 $
 
 Example input:  
 ```
 $ python movies.py show_movies high_box_office
 ```
 
 
 **6. _compare_ command - compare two movies and show which one is more successful in the selected category**
 
 Command pattern: movies.py compare column movie_title movie_title
 
 where:  
  _category_ is one option from list: imdb_rating, box_office, awards_won, runtime, awards_won, award_nominations, oscar_nominations, oscars_won
 _movie_title_ is title of one of the movies you want to compare. If the name of the movie consist of more than one word, use underscores instead of spaces. _movie_title_ is case insensitive.  
 
  Example input:  
  ```
 $ python movies.py compare awards_won inception toy_story
 ```
 
 Take into consideration that the comparison is not always possible due to the lack of necessary data about the movie. In that case, you will be notified by an appropriate message.
 
 
 **7. _highscores_ command - show current top values in following categories: runtime, bo office earnings, awards won, nominations, Oscars won, IMDB rating**
 
  Command pattern: movies.py highscores
  
  Eample input:  
  ```
  $ python movies.py highscores
  ```
  
  This command does not require or accept any additional arguments.
  
