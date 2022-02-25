"""
In order to get this script working, you must set an environmental variable
that specifies the name of this file.

Commands to specify environmental variable in PowerShell:
set FLASK_APP=hello.py
$env:FLASK_APP = "hello.py"
flask run
"""

from flask import Flask, jsonify, request, json

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

'''
Method: GET
Description: Confirms that the api is up and working.
'''
@app.route("/", methods = ['GET'])
def get_api_status():
  return_json = {"status_code": f"200", "Note": "OK. Request has succeeded.", "Message": "The API is up and running!"}
  return jsonify(return_json)

'''
Method: GET
Description: Gets all database information.
'''
@app.route("/allData", methods = ['GET'])
def get_all_data():
  f = open('database.json')
  data = json.load(f)
  return jsonify(data)

'''
Method: GET
Description: Gets the amount of choices there could be.

Method: POST
Description: Changes the amount of choices there could be.
Variable name: choiceCount
'''
@app.route("/numberOfChoices", methods = ['GET', 'POST'])
def number_choices():

  # Specifying the location of our database file
  database_file = "database.json"

  # Opening our database file as a file object
  with open(database_file) as database_file:

    # Converting out file object to a json object
    database_decoded = json.load(database_file)

    # Getting the number of choices we have
    count = 0
    for key in database_decoded:
      if "movie_choice_" in key:
        count += 1

    # If the request is a GET request
    if request.method == "GET":

      return_json = {"count": f"{count}", "Note": "This is the amount of options users can pick from."}
      return jsonify(return_json)

    # If the reqeust is a POST request
    if request.method == "POST":

      # Specifying that the request is a JSON just in case the developer did not include that in their header
      request_data = request.get_json()

      # Converting from string to int so we can use it to iterate
      choiceCount = int(request_data["choiceCount"])

      # Run while choiceCount is not equal to count
      while choiceCount != count:

        # If choiceCount is greater than count
        if choiceCount > count:
          count += 1
          database_decoded["movie_choice_" + count] = "null"
        else:
          # Deleting choices until choiceCount is equal to count
          del database_decoded["movie_choice_" + count]
          count -=1

        return_json = {"status_code": "200", "Note": "OK. Request has succeeded."}
        return jsonify(return_json)
  
  # This only happens if the user did not submit either a GET or POST request
  return_json = {"status_code": "400", "Note": "Bad Request. This endpoint only handles GET and POST requests."}
  return jsonify(return_json)

'''
Method: GET
Description: Gets the specified movie choice.
Variable: 
  - choiceNumber: Which choice to modify.

Method: POST
Description: Changes the movie choice to whatever the user specified.
Variable: 
  - choiceNumber: Which choice to modify.
  - choiceName: String to change the name to.

'''
@app.route("/movieChoice", methods = ['GET', 'POST'])
def movie_choice():

  # Specifying the location of our database file
  database_file = "database.json"

  # Specifying that the request is a JSON just in case the developer did not include that in their header
  request_data = request.get_json()

  # Opening our database file as a file object
  with open(database_file) as database_file:

    # Converting out file object to a json object
    database_decoded = json.load(database_file)

    # If the request is a GET request
    if request.method == "GET":
      movie = database_decoded["movie_choice_" + request_data["choiceNumber"]]

      return_json = {"status_code": "200", f'{database_decoded["movie_choice_" + request_data["choiceNumber"]]}': movie}
      return jsonify(return_json)

    if request.method == "POST":

      # If the choice name is a valid movie option
      if request_data["choiceName"] in database_decoded["all_movies_list"]:
        database_decoded["movie_choice_" + request_data["choiceNumber"]] = request_data["choiceName"]

        return_json = {"status_code": "200", f'{database_decoded["movie_choice_" + request_data["choiceNumber"]]}': movie}
        return jsonify(return_json)
      else:
        return_json = {"status_code": "400", "Note": 'Bad Request. choiceName does not match any movie option found in all_movies_list. Go to endpoint "/allData" and look at all_movies_list for a full list of valid movie options.'}
        return jsonify(return_json)

  # This only happens if the user did not submit either a GET or POST request
  return_json = {"status_code": "400", "Note": "Bad Request. This endpoint only handles GET and POST requests."}
  return jsonify(return_json)

'''
Method: GET
Description: Gets a list of all movies available.

Method: POST
Description: Adds or removes a movie from the list of available movies.
Variables:
  - movieName: name of the movie to add to the list of valid movies ("all_movies_list").
'''
@app.route("/allMovies", methods = ['GET', 'POST'])
def all_movies():

  # Specifying the location of our database file
  database_file = "database.json"

  # Specifying that the request is a JSON just in case the developer did not include that in their header
  request_data = request.get_json()

  # Opening our database file as a file object
  with open(database_file) as database_file:

    # Converting out file object to a json object
    database_decoded = json.load(database_file)

    # If the request is a GET request
    if request.method == "GET":

      return_json = {"status_code": "200", "all_movies_list": database_decoded["all_movies_list"]}
      return jsonify(return_json)

    # If the request is a POST request
    if request.method == "POST":

      movieName = request_data["movieName"]

      database_file["all_movies_list"].append(movieName)

      return_json = {"status_code": "200", "Message": "Movie has been added."}
      return jsonify(return_json)
  
  # This only happens if the user did not submit either a GET or POST request
  return_json = {"status_code": "400", "Note": "Bad Request. This endpoint only handles GET and POST requests."}
  return jsonify(return_json)
