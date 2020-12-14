To: Players
From: Nicholas Ding and Michael Tang
Date: 10/08/2020
Subject: System Data Representation


The system will contain multiple methods for the communication with players in order to give players necessary information to play the game, and to allow the players to make moves.

Input:

For input from the players to the system, the system will only accept a Json dictionary containing three fields with specific labels:
-	Labeled “move” will be a Json tuple containing two integers, an x value and a y value for the next move the player wants to make.  These moves will include placing penguins initially and moving the penguins once the game starts.
-	Labeled “user” will be a Json string, containing the username of the player involved in the move
-	Labeled “pass” will be a Json string, containing the unique password set by the user to insure the move actually came from the user themselves.
These values in the dictionary will help insure both that the player’s moves are received by the system, and that the player sending the moves to the system is actually the player who should be sending the move.  An example of a user input is as follows:
{“Move”:(1,2),“User”:“ImBadAtCoding”,“Password”:“ThisIsMyPassword”}



Output:
The system will output information to the users in two different ways.

For the passing of non-gamestate information, such as the end of the game, invalid moves or other errors that may take place, the system will send a Json String to users.

For the passing of gamestate information, the system will pass a Json dictionary to users, containing 3 fields with specific labels:
-	Labeled “Board” will be a Json Dictionary containing tuples corresponding to each tile in the board as labels, and the point value of each tile as a value.  
An empty tile will be denoted with a point value of 0
-	Labeled “Scores” will be a Json Dictionary containing each players username as labels, and the respective players point total as values
-	Labeled “Penguins” will be a Json Dictionary containing each players username as labels, and a tuple containing the respective penguins tuple as a value.
An example of a game state output is as follows:
{“Board” : {(0,0):1 , (0,1):3 , (0,2):0, (1,0):5 , (1,1):2 , (1,2):1)},
“Scores” : {“Player1”:3 , “Player2”: 5},
“Penguins” : {“Player1”: (0,1) , “Player2”: (1,0)}}
