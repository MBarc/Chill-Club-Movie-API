"""
In order to get this script working, you must set an environmental variable
that specifies the name of this file.

Commands to specify environmental variable in PowerShell:
set FLASK_APP=main.py
$env:FLASK_APP = "main.py"
flask run
"""
import random
import os
from pymongo import MongoClient
from flask import Flask, jsonify, request, json, Response
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId # used for getting/specifying certian documents
from bson import json_util

app = Flask(__name__)
cors = CORS(app)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

# Variables to establish mongodb connection
username = os.environ["MONGODB_USER"]
password = os.environ["MONGODB_PASS"]
hostname = os.environ["HOSTNAME"]
port = os.environ["PORT"]

# Establishing a connection to the mongodb
client = MongoClient(f"mongodb://{username}:{password}@{hostname}:{port}/?authMechanism=DEFAULT")

# Navigating to the movietheater database
db = client['api_movietheater']

def document_count(collection):
    """
    Returns the amount of documents are in a collection.
    """

    return len(list(collection.find()))

def write_document(collection, key, value):
    """
    Writes document to collection.
    """

    payload = {key: value}

    collection.insert_one(payload)

def remove_document(collection, key, value):
    """
    Remove document from collection
    """

    payload = {key: value}

    collection.delete_one(payload)

def edit_document(collection, document_ObjectID, key, value):
    """
    Edit/changes a document
    """

    myquery = {'_id': document_ObjectID}
    newvalues = {'$set': {key : value}}

    collection.update_one(myquery, newvalues)

def validate_token(token):
  """
  Vlidates a users token/authorization to use this api.
  """

  # Establishing a connection to the mongodb
  client = MongoClient(f"mongodb://{username}:{password}@{hostname}:{port}/?authMechanism=DEFAULT")

  # Navigating to the tokens database
  db = client['tokens']

  # Navigating to the right collection
  collection = db['tokens']

  for document in collection.find():

    if "token" in document:

      if document["token"] == token:

        return True

  return False

def get_variable(request, variable_name):
  """
  Returns the variable whether or not the request is a get or post request.
  
  variable_name (str): the name of the variable to get in the request.
  """

  # This gets declared if get request
  variable = request.args.get(variable_name) # gets declared if get request
  
  # If variable was not declared. . .
  if not variable:

    # . . . this get gets declated if post request
    variable = str(request.get_json()[variable_name]) # gets declared if post request

  return variable

'''
Method: GET
Description: Confirms that the api is up and working.
'''
@app.route("/", methods = ['GET'])
def get_api_status():
  return_json = {"Message": "The API is up and running!"}
  #return_json = {"status_code": f"200", "Message": "OK. Request has succeeded.", "Message": "The API is up and running!"}
  #return jsonify(return_json)
  return jsonify(return_json), 200


'''
Method: GET
Description: Gets all database information.
'''
@app.route("/allData", methods = ['GET'])
def get_all_data():

  # The token the user provide ; we'll use this to authorize the request
  token = get_variable(request, "token")

  # If the token provided is not valid
  if not validate_token(token):
    return_json = {"Message": "Token provided is not valid."}
    return jsonify(return_json), 400

  # Putting all the data here
  allData = {}

  # For each collection in the database
  for col in db.list_collection_names():

    # Declaring the key as a list
    allData[col] = []

    # For each document in the collection
    for doc in db[col].find():

      # Adding the document to the list
      allData[col].append(doc)
      
  # Returning everything has a json
  return jsonify(json.loads(json_util.dumps(allData)))

'''
Method: GET
Description: Gets the amount of choices there could be.

Method: POST
Description: Changes the amount of choices there could be.
Variable name: 
  - choiceCount: The amount of choices you want there to be.
'''
@app.route("/numberOfChoices", methods = ['GET', 'POST'])
def number_choices():

  # The token the user provide ; we'll use this to authorize the request
  token = get_variable(request, "token")

  # If the token provided is not valid
  if not validate_token(token):
    return_json = {"Message": "Token provided is not valid."}
    return jsonify(return_json), 400

  # Navigating to the right collection
  collection = db['poll']

  #  Getting the amount of documents in the collection by using a wildcard filter ({})
  count = collection.count_documents({})

  # If the request is a GET request
  if request.method == "GET":

    return_json = {"count": f"{count}", "Note": "This is the amount of options users can pick from."}
    return jsonify(return_json)

  # If the reqeust is a POST request
  if request.method == "POST":

    # Specifying that the request is a JSON just in case the developer did not include that in their header
    request_data = json.loads(request.data, strict=False)

    newCount = int(request_data["choiceCount"])

    # Add a movie if the choice count has increased
    if newCount >= count:

      # While newCount and count are not equal
      while newCount != count:

        count += 1

        randomMovie = random.choice(list(db['all_movies'].find()))["title"]

        write_document(collection, f"movie_choice_{count}", randomMovie)

    else: # Remove a movie if the choice count has decreased

      while newCount != count:

        count -= 1

        documentToRemove = list(collection.find())[document_count(collection)-1]["_id"]

        remove_document(collection, "_id", documentToRemove)

    return_json = {"Note": "OK. Request has succeeded."}
    return jsonify(return_json), 200

  
  # This only happens if the user did not submit either a GET or POST request
  return_json = {"Message": "Bad Request. This endpoint only handles GET and POST requests."}
  return jsonify(return_json), 400

'''
Method: GET
Description: Gets the specified movie choice.
Variable: 
  - choiceNumber: The number of the specific choice you want to get.

Method: POST
Description: Changes the movie choice to whatever the user specified.
Variable: 
  - choiceNumber: Which choice to modify.
  - choiceName: String to change the name to.

'''
@app.route("/movieChoice", methods = ['GET', 'POST'])
def movie_choice():

  # The token the user provide ; we'll use this to authorize the request
  token = get_variable(request, "token")

  # If the token provided is not valid
  if not validate_token(token):
    return_json = {"Message": "Token provided is not valid."}
    return jsonify(return_json), 400

  collection = db["poll"]

  choiceNumber = str(get_variable(request, "choiceNumber"))

  for choice in collection.find():

    if f"movie_choice_{choiceNumber}" in choice:

      movieChoice = choice

  # If the request is a GET request
  if request.method == "GET":

    return_json = {f"movie_choice_{choiceNumber}": movieChoice}
    return jsonify(json.loads(json_util.dumps(return_json))), 200

  if request.method == "POST":

    choiceName = str(get_variable(request, "choiceName"))

    for choice in collection.find():

      if f"movie_choice_{choiceNumber}" in choice:

        edit_document(collection, choice["_id"], f"movie_choice_{choiceNumber}", choiceName)
        edit_document(collection, choice["_id"], "votes", 0)

    else:
      return_json = {"Message": 'Bad Request. choiceName does not match any movie option found in all_movies_list. Go to endpoint "/allMovies" and look at all_movies_list for a full list of valid movie options.'}
      return jsonify(return_json), 400

  # This only happens if the user did not submit either a GET or POST request
  return_json = {"Message": "Bad Request. This endpoint only handles GET and POST requests."}
  return jsonify(return_json), 400

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

  # The token the user provide ; we'll use this to authorize the request
  token = get_variable(request, "token")

  # If the token provided is not valid
  if not validate_token(token):
    return_json = {"Message": "Token provided is not valid."}
    return jsonify(return_json), 400

  # Navigating to the right collection
  collection = db['all_movies']

  # If the request is a GET request
  if request.method == "GET":

    all_movies = [movie['title']for movie in collection.find()]
    
    return_json = {"all_movies_list": all_movies}
    return jsonify(return_json), 200

  # If the request is a POST request
  if request.method == "POST":

    request_data = json.loads(request.data, strict=False)

    movieName = request_data["movieName"]

    if request_data["operation"] == "add":

      write_document(collection, "title", movieName)

      return_json = {"Message": "Movie has been added."}
      return jsonify(return_json), 200

    if request_data["operation"] == "remove":

      remove_document(collection, "title", movieName)

      return_json = {"Message": "Movie has been removed."}
      return jsonify(return_json), 200

    # This only happens if the user did not submit either a GET or POST request
    return_json = {"Message": 'Bad Request. Operation variable can only be "add" or "remove"'}
    return jsonify(return_json), 400

'''
Method: GET
Description: Gets the current movie theater password.

Method: POST
Description: Changes/updates the movie theater password.
Variables:
  - password: The password to change the movie theater password to.
'''
@app.route("/movieTheaterPassword", methods = ['GET', 'POST'])
@cross_origin()
def movie_theater_password():

  # The token the user provide ; we'll use this to authorize the request
  token = get_variable(request, "token")

  # If the token provided is not valid
  if not validate_token(token):
    return_json = {"Message": "Token provided is not valid."}
    return jsonify(return_json), 400

  collection = db["password"]

  password_ObjectId = ObjectId("62a2511cbfb1daf6e9dec5c2")

  # If the request is a GET request
  if request.method == "GET":

    password = collection.find_one(password_ObjectId)["password"]

    return_json = {"movie_theater_password": password}
    return jsonify(return_json), 200

  # If the request is a POST request
  if request.method == "POST":

    request_data = json.loads(request.data, strict=False)

    edit_document(collection, password_ObjectId, "password", request_data["password"])

    return_json = {"Message": "Movie theater password has been updated!"}
    return jsonify(return_json), 200

  # This only happens if the user did not submit either a GET or POST request
  return_json = {"Message": "Bad Request. This endpoint only handles GET and POST requests."}
  return jsonify(return_json), 400

'''
Method: GET
Description: Returns the message id.

Method: POST
Description: Changes the message id.
Variables:
  - id: The id to change the message id to.
'''
@app.route("/pollmessageid", methods = ['GET', 'POST'])
def poll_message_id():
  
  # The token the user provide ; we'll use this to authorize the request
  token = get_variable(request, "token")

  # If the token provided is not valid
  if not validate_token(token):
    return_json = {"Message": "Token provided is not valid."}
    return jsonify(return_json), 400

  collection = db["poll_message_id"]

  # If the request is a GET request
  if request.method == "GET":

    for choice in collection.find():

      if "id" in choice:

        poll_id = choice["id"]

    return_json = {"id": poll_id}
    return jsonify(return_json), 200


  # If the request is a POST request
  if request.method == "POST":

    # The token the user provide ; we'll use this to authorize the request
    poll_id = get_variable(request, "id")

    # Deleting every document in the collection
    collection.delete_many({})

    # Writing the id as a document
    write_document(collection, "id", poll_id)

    return_json = {"Message": "Movie theater password has been updated!"}
    return jsonify(return_json), 200

  # This only happens if the user did not submit either a GET or POST request
  return_json = {"Message": "Bad Request. This endpoint only handles GET and POST requests."}
  return jsonify(return_json), 400
  
'''
Method: GET
Description: Returns the list of movies that have won the poll.

Method: POST
Description: Clears out the previous winning choices and adds in the new ones.
Variables:
  - listOfChoices: The list of the winning choices.
'''
@app.route("/winningChoices", methods = ['GET', 'POST'])
def winning_choices():

  # The token the user provide ; we'll use this to authorize the request
  token = get_variable(request, "token")

  # If the token provided is not valid
  if not validate_token(token):
    return_json = {"Message": "Token provided is not valid."}
    return jsonify(return_json), 400

  collection = db["winning_choices"]
  
  # If the request is a GET request
  if request.method == "GET":

    movie_list = [movie["title"] for movie in collection.find()]

    return_json = {"winning_choices": movie_list}
    return jsonify(return_json), 200

  # If the request is a POST request
  if request.method == "POST":

    # Getting the list of choices and converting to list
    listOfChoices = get_variable(request, "lifeOfChoices")
    listOfChoices = listOfChoices.split(",")

    # Deleting every document in the collection
    collection.delete_many({})

    for choice in listOfChoices:
      write_document(collection, "title", choice)

    return_json = {"Message": "Winning choices have been updated!"}
    return jsonify(return_json), 200
  
  # This only happens if the user did not submit either a GET or POST request
  return_json = {"Message": "Bad Request. This endpoint only handles GET and POST requests."}
  return jsonify(return_json), 400

if __name__ == "__main__":
    port = int(os.environ["API_PORT"])
    app.run(debug=True, host='0.0.0.0', port=port)
