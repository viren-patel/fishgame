# A Specification Player Referee Interactions

Author: Nicholas Ding and Michael Tang
Repo: BigSandy

## Players

Players must be created based off the abstract class located within Common/player_interface.py.  This class contains the necessary functionality
for a player to communicate with the referee.

## Referee to Player Functions

recieve_gamestate(self, gamestate : dict)
  Recieve Gamestate is called by the referee to give a gamestate to the player.
  A gamestate will be given to a user after each valid move is played in the game.
  The format of the dictionary of a gamestate is as follows:
            {“Board” : [[1,2,3],[4,0,5],[1,1,0]],
            “Scores” : {“Blue”:3 , “Red”: 5},
            “Players” : {"Blue" : {"score" : 3, "color" : "Blue", "penguins" : [(0,0)]},
                         "Red" : {"score" : 2, "color" : "Red", "penguins" : [(1,0)])},
            "Turns" : ["Blue" , "Red"]}



receive_error(self, errormessage : dict)
  Receive Gamestate is called by the referee to signal to the user that an illegal move was attempted

  The errormessage dictionary will contain a value under "Type", which specifies the type of illegal move that occurred.
    The possible values under "Type" are as follows:
      "placement" - This signifies that the user attempted to place a penguin in an illegal spot
      "out of turn" - This signifies that the user attempted to move out of turn
      "move from location" - This signifies that the user attempted to move from a location in which they did not have a penguin
      "move to location" - This signifies that the user attempted to move a penguin to a location the penguin could not reach

  The errormessage dictionary will also contain a text explanation of the illegal move under "Message"

  Ex:
              {"Type" : "placement",
              "Message" : "There is already a penguin in that spot."}

              or

              {"Type" : "move to location",
              "Message" : "This penguin can not reach that location"}

## Player to Referee Functions:
  Functions in which the referee requests information from the player have a time limit.
  If a player fails to respond within the limit, their turn may be skipped or they may be disqualified.
  Players will not be skipped or disqualified over illegal moves.
    However making an illegal move does not reset the time limit for the player to make a legal move.


place_penguin(self)
  Place penguin is called by the referee to request that the player place a penguin.

  The player will be given a set amount of time to select a location and report back to the referee.
  If a user fails to respond to the referee in time, the user will be disqualified from the competition and skipped over in following rounds.

  The function must return a tuple (x, y) representing the x and y coordinates on the board where the player wishes to place the penguin


send_next_move(self):
  Send next move is called by the referee to request that a player play a move.

  The player will be given a set amount of time to select a move and report back to the referee.
  If a user fails to respond to the referee in time, the user will be skipped for this move
  If a user is skipped two moves in a row, the user is disqualified and skipped over in following rounds

  The function must return two tuples.
    The first tuple (start_x, start_y) represents the x and y coordinates on the board of the penguin the player wishes to move
    The second tuple (end_x, end_y) represents the x and y coordinates on the board where the player wishes to move the penguin to

identify(self)
  Identify is used by the referee to help identify the user at the beginning and end of the game.

  The player will be given a set amount of time to return information back to the referee.
  If a user fails to respond to the referee in time, the user will be disqualified and skipped over in following rounds.

  The function must return a dictionary with keys as follows:
              {"Name" : "Player 1",
               "Age" : "20"}
