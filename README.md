# Chill Club's Movie Theater API

This API is responsible for connecting different technologies that Chill Club uses for movie nights.

## Endpoints

```

Endpoint: /
GET: Confirms that the api is up and working.

Endpoint: /allData
GET: Gets all database information.
	Variables:
		token (str): movietheater_api token that authorizes the request.
	Example: http://api-movietheater.chillclub.online:5555/allData?token=XXXXXXXXXXXXXXXXXXXX

Endpoint: /numberOfChoices
GET: Gets the amount of choices there could be.
	Variables:
		token (str): movietheater_api token that authorizes the request.
	Example:  http://api-movietheater.chillclub.online:5555/numberOfChoices?token=XXXXXXXXXXXXXXXXXXX
POST: Changes the amount of choices there could be.
	Variables:
		token (str): movietheater_api token that authorizes the request.
		choiceCount (int): The amount of choices you want there to be.
		
Endpoint: /movieChoice
GET: Gets the specified movie choice.
	Variables:
		token (str): movietheater_api token that authorizes the request.
		choiceNumber (int): The number of the specific choice you want to get.
	Example: http://api-movietheater.chillclub.online:5555/movieChoice?token=XXXXXXXXXXXXXXXXXXX&choiceNumber=1
POST: Changes the movie choice to whatever the user specified.
	Variables:
		token (str): movietheater_api token that authorizes the request.
		choiceNumber (int): Which choice to modify.
		choiceName (str): String to change the name to.
		
Endpoint: /allMovies
GET: Gets a list of all movies available.
	Variables:
		token (str): movietheater_api token that authorizes the request.
	Example: http://api-movietheater.chillclub.online:5555/allMovies?token=XXXXXXXXXXXXXXXXXXX
POST: Adds or removes a movie from the list of available movies.
	Variables:
		token (str): movietheater_api token that authorizes the request.
		movieName: name of the movie to add to the list of valid movies ("all_movies_list").
		
Endpoint: /movieTheaterPassword
GET: Gets the current movie theater password.
	Variables:
		token (str): movietheater_api token that authorizes the request.
	Example: http://api-movietheater.chillclub.online:5555/movieTheaterPassword?token=XXXXXXXXXXXXXXXXXXX
POST:Changes/updates the movie theater password.
	Variables:
		token (str): movietheater_api token that authorizes the request.
		password: The password to change the movie theater password to.
		
Endpoint: /pollmessageid
GET: Returns the message id.
	Variables: 
		token (str): movietheater_api token that authorizes the request.
	Example: http://movietheater-api.chillclub.online:5555/pollmessageid?token=XXXXXXXXXXXXXXXXXXX
POST: Changes the message id.
	Variables:
		token (str): movietheater_api token that authorizes the request.
		id: The id to change the message id to.
	
Endpoint: /winningChoices
GET: Returns the list of movies that have won the poll.
	Variables:
		token (str): movietheater_api token that authorizes the request.
	Example: http://api-movietheater.chillclub.online:5555/winningChoices?token=XXXXXXXXXXXXXXXXXXX
POST:
	Variables:
		token (str): movietheater_api token that authorizes the request.
		listOfChoices: The list of the winning choices.

