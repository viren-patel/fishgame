To: Sub-contractor in the far-away land of Codemanistan
From: Nicholas Ding and Michael Tang
Date: 10/08/2020
Subject: Tournament Manager Protocol

The tournament manager handles setting up tournaments for players and referees, and allows observers to watch the tournament.

Internal Setup:
  Functions:

    void open_signups() | Function that opens the signups for the tournament allowing users to play.  This phase lasts 20 minutes
    void make_tournament() | Creates the bracket for the tournament once user signups have ended
    void check_round_finish() | Checks if all referees have finished the games for a round of the tournament
    void next_round() | Sets up the tournament for the next round of games.  Sends out updates to players about AI progress.
    void declare_winner() | Sends out a message to players about the winner of the tournament.  Sends prizes to winner.


The manager must be able to interact with these three external groups of participants in the tournament: players, referees, and observers.

Players:
  The tournament must be able to take in the information of players in the games.  It must also be able to communicate tournament results back to the corresponding competitors as AIs are eliminated.  In order to do so, the tournament must have functionality to receive sign ups, and send messages to players who have signed up

  Functions:
    void sign_up_player | Signs up a player for the tournament
    void send_results | Sends the results to players.  Results include all player rankings, and those who are moving on to the next round.

Referees:
  The tournament must be able to make the proper amount of referees to play the games within the tournament.  It must also have functionality to speak to the referees, handing the players and gamestate to the referee to start the game, and receiving the results of the game from the referee once the game is finished.

  Functions:
    void set_up_game | Sets up the game by creating a gamestate and a referee.  Gives players and gamestate to referee.  The referee recieves the players in a list in the order of their turn order.
    void get_result | Gets the result of the game from the referee.
    void get_current_gamestate | Gets the gamestate of the game from the referee.  Used for getting gamestates to give to observers.



Observers:
  The tournament must be able to handle having observers who are neither referees nor competitors but are there to watch the games.  Thus, It must have functionality to receive game update requests from the observers, request the gamestate from the referee, and return it to the observer who requested it.

  Functions:
    void get_request | Allows observers to request the current gamestate of a given game.
    void return_current_games  |  Allows observers to ask for a list of current games and the AIs involved in each game.
    void return_gamestate  |  Returns the gamestate the observer requested.
