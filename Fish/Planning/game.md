To: Players, Referees, and Administrators
From: Nicholas Ding and Michael Tang
Date: 10/15/2020
Subject: Game Representation

Game

Players and Referees will need an interface which will allow them to check for valid moves, and plan further action.  Thus, a new Game class will be created in order to give the players and the referees the ability to check possible moves, and plan.  The Game will function by saving a gamestate, and allowing the user to check if a move is valid, and make the move to the game state.  In order to help users plan, the game will also be able to move back from a gamestate, allowing users to predict moves by their opponent, and go back if their predictions are not correct.


Functions:
	list turn_order()
	 Turn order returns a list of player names, with players in order of when it will be their turn.

  boolean check_valid_move(x_coord : int , y_coord : int)
    Check valid move is a boolean representing whether the player who has the current turn is able to move to the location on the board represented by the point (x_coord,y_coord).

	list check_available_moves()
	 Check Available moves returns a list of available moves for the player with the current turn.  The list consists of tuples (x,y) with x representing the x coordinate and y representing the y coordinate of each point on the board which the current player is able to move to

  void make_moves(moves : list)
    make moves allows a player to plan ahead, by making moves projected moves for themselves and their opponents.  The function takes in moves, a list of tuples (x,y) with x representing the x coordinate and y representing the y coordinate of the different moves.  Moves are played in based off the current turn order of the players.  If an invalid move is inputted, the function stops at that move, and throws an error.

  void undo_moves(num : int):
 	  undo moves allows a user to undo projected moves and return the state of Game to an older state.  This allows for further testing without the need for multiple games.

  Dict get_game_state():
	 Get game state returns the current state of the game, and allows users to see the board and plan after moves have been made.  The dictionary outputs a dictionary with 3 pairs of keys and values.
      -	Labeled “Board” will be a two dimensional list containing the point value of all the tiles on the board.
      An empty tile will be denoted with a point value of 0
      -	Labeled “Scores” will be a dictionary containing each players name as labels, and the respective players point total as values
      -	Labeled “Penguins” will be a Dictionary containing each players username as labels, and a tuple containing the respective penguins tuple as a value.
      - Labeled "Turns" will be a list of player names in order based off of the turn order.
      {“Board” : [[1,2,3],[4,0,5],[1,1,0]],
      “Scores” : {“Player1”:3 , “Player2”: 5},
      “Penguins” : {“Player1” (0,1) , “Player2”: (1,0)}
      "Turns" : ["Player1" , "Player 2"]}
