# Movie Theater

Udacity Full stack Nanodegree Capstone Project
This project is a mimic of the popular AMC app which allows you to view the showtime based 
on movies or theaters of your choice.

# API URL

Heroku: https://capstone-app-08222.herokuapp.com/

Localhost: base URL is localhost:5000

# Features

Create and manage theaters and movies, also allows a manager to add showtimes for a movie in
a particular theater.

Authentication is implemented in the form of Role Based Access Control using Auth0

# Roles

**Public**: Can view movies, theaters info and showtimes; can search on the website based on
the movie title;

**Theater manager**: Can perform all operations including adding and deleting a movie/theater, 
and the corresponding showtime info will also be added/deleted.

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, create a database named ```theater```

For testing, create a database named ```theater_test```

### Running the server

From within the `./starter` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Endpoints
Below shows the documentation of the endpoints in this project:

The format of this documentation:
- Endpoint
- Function
- Request Arguments
- Return


GET '/movies'
- Fetches a dictionary of categories in which the key is the movie_info and the values are the corresponding string of movie details.
- Request Arguments: None
- Returns: An object with a single key, movie_info, with the corresponding value being the list of all the movies. 

"movie_info": 

     [{ "movie_description":"a",
        "movie_id":1,
        "movie_image":"a",
        "movie_review":"a",
        "movie_trailer":"a"}]

GET '/movies/1'
- Fetches a movie based on movie_id. 
- Request Arguments: movie_id
- Returns: The showtime info of this movie, including the theater info and exact showtime which
is an array of time.

"showtime_info":

    [{"address":"a",     
    "showtime":["12:00","14:30"], 
    "theater_id":1,  
    "theater_name":"a",  
    "website":"a"}]

DELETE 'movies/1'

- Deletes a specified movie
- Request Arguments: jwt, movie_id
- Returns: HTTP status code and the id of the movie if succeeded. 

POST '/movies/search'

- Search a movie by title
- Request Arguments: Body
- Returns: All the movies whose title match the search_term


POST '/movies'

- Create a new movie 
- Request Arguments: jwt, Body
- Returns: HTTP status code and json object {"success": True,} if successfully created a question. Else, return only the error message(see Error Handling section for details)

GET '/theaters'

- Fetches all the theaters available
- Request Arguments: None
- Returns: An object with a single key: movie_info, with the corresponding value being a list 
of all the theaters available

"movie_info":

    [{"theater_address":"a", 
    "theater_id":1,
    "theater_name":"a",
    "theater_phone":"a",
    "theater_website":"a"}]

POST '/theaters'

- Post a new theater
- Request Arguments: jwt, Body
- Returns: HTTP status code and json object {"success": True,} if successfully created a question. Else, return only the error message(see Error Handling section for details)

DELETE '/theaters/1'

- Delete a theater by theater_id 
- Request Arguments: jwt, theater_id 
- Returns: HTTP status code and the id of the theater if succeeded

POST '/showtimes/create'

- Post a new showtime info based on movie_id and theater_id
- Request Arguments: jwt, Body {'movie_id': 1, 'theater_id': 1, 'start_time': ['11:30']}
- Returns: HTTP status code

## Testing
To run the tests, run

python test_app.py

Authentication and Authorization test results are exported to Capstone-movie-theater
.postman_collections.json

## Error Handling
Errors are returned as json objects with the following format:
{
    "success": False,
    "error": 400,
    ""message": bad request
}

The API will return 4 types of errors:
- 400: bad request
- 404: resource not found
- 405: method not allowed
- 422: unprocessable