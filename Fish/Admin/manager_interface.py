from Common.state import State
"""
manager_interface - The manager interface is an abstract class built to represent the basic functionality necessary to run a tournament.
                    The class includes functions designed to allow the tournament to communicate with referees, players and observers while running the tournament.
"""

class manager_interface:
    """#################################################   Internal Functions #####################################################"""
    #open_signups - Functions called on the manager to open signups for the tournament.  Signups last 20 minutes.
    def open_signups(self):
        pass

    #make_tournament - Function for creating the bracket of the tournament with the players that have signed up.
    def make_tournament(self):
        pass

    #check_round_finish - Function that goes through all created games and checks if all games are finished.
    def check_round_finish(self):
        pass

    #next_round - function that creates games for the next round of the tournament
    def next_round(self):
        pass

    #declare_winner - Function that ends a message to all players on who won the tournament.  This function also sends the prize to the winner.
    def declare_winner(self):
        pass

    """#################################################   Player Functions #####################################################"""
    #sign_up_player - signs up a player for the tournament after recieving a player signup
    def sign_up_player(self, player):
        pass
    #send_results - sends the results of an individual game that this player participated in to the player.  Informs a player if their AI has advanced.
    def send_results (self):
        pass

    """#################################################   Referee Functions #####################################################"""
    #set_up_game - Sets up a game by creating a board and referee.  Gives referee the board and players which is a list of players in their turn order.
    def set_up_game (self, players):
        pass
    #get_result - Gets the result of the game with id game_id from the proper referee if the game has finished.  Returns false if the game is not over.
    def get_result(self, game_id):
        pass
    #get_current_gamestate - Gets the current gamestate of the game with id game_id from the proper referee.  Used to allow observers to observe games
    def get_current_gamestate (self,game_id):
        pass
    """#################################################   Observer Functions #####################################################"""
    #get_request - gets a request for a gamestate (at game_id) form the observer.  Keeps track of observer that asked for it.
    def get_request (self, observer, game_id):
        pass
    #return_current_games - sends the observer a list of games which includes the AIs participating in the games and the game_id
    def return_current_games(self, observer):
        pass
    #return_gamestate - returns the gamestate of game_id to the obeserver.
    def return_gamestate(self, observer, game_id):
        pass
