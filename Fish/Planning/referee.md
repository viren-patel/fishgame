To: Sub-contractor in the far-away land of Codemanistan
From: Nicholas Ding and Michael Tang
Date: 10/08/2020
Subject: Referee for Fish Tournament

The referee class will have the responsibility of running a single game of the tournament.  It will need to be able to communicate with both players and the tournament in order to do so, and must be able to handle the different stages of the game: start, placing penguins, moving penguins, and end.


void start_game (player_ai : List[player_interface], penguins_per_player : Integer):
  The play game function handles the setting up of the game.  It takes in a list of all the player AIs, in order based off of their turn order and the dimensions of the board (height, width).  The function then creates the board for the game and saves the list of players to a local variable.  The function then moves the referee to the run_game function to start the playing of the game.

void run_game(board : List[List[[Integer]], penguins_per_player : Integer):
  The run game function goes through the steps of running a Fish game.  The run game function guides the referee through the three steps in running a game: placing penguins, moving penguins, and end.

void place_penguins(penguins_per_player : Integer):
  The place penguins method handles the part of the game in which penguins are placed on the board.  The referee calls on players in order requesting a penguin placement, and responding with either an error message or a message stating that the penguin was placed.  If a player fails to respond to the referee after a 5 second wait, the player is considered disconnected and all their penguins are removed from the board.

void move_penguins():
  The move penguins method handles the part of the game in which players move their penguins across the board.  The referee calls on players in order requesting a move, and responding with either an error message or a message stating that the move occurred.  If a player fails to respond to the referee after a 5 second wait, the player is skipped for this turn.  After a player is skipped for 2 of their turns in a row, the player is considered disconnected and all their penguins are removed from the board.  move_penguins calls check_game_end between turns to check whether the game has ended.

end_game():
  This function is called at the end of the game, when no penguins are able to make any more moves on the board.  This function handles the final scorekeeping, as well as the reporting of the placement of players back to the tournament.

remove_player(player : player_interface):
  This function removes a player from the game.  It is called when a player is disconnected, and removes all the players penguins from their turn, and the player from the turn order.

remove_penguin(loc : (x , y)):
  This function is called to remove a penguin from the board.  It removes the penguin located at loc, a tuple x,y of integers representing the x and y coordinates of the penguin.  Penguins are removed from the board either when a player is disconnected, or a penguin has no moves remaining on the board.

send_gamestate():
  This function is called at the beginning of the game, and after every valid penguin placement, or move.  It sends a gamestate to each player in the game.

check_game_end():
  This function is called to see whether any penguin has a possible move on the board.  If no penguin is able to move, this function declares that the game is over.

report_winner(winner : player_interface):
  This function reports the player with the highest score to the tournament.
