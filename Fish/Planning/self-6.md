## Self-Evaluation Form for Milestone 6

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

The implementation of the "steady state" phase of a board game
typically calls for several different pieces: playing a *complete
game*, the *start up* phase, playing one *round* of the game, playing a *turn*,
each with different demands. The design recipe from the prerequisite courses call
for at least three pieces of functionality implemented as separate
functions or methods:

- the functionality for "place all penguins"
https://github.ccs.neu.edu/CS4500-F20/bigsandy/blob/9b1e1a15623f75a3e87c7e076d7aad0cb5704503/Fish/Admin/referee.py#L58
- a unit test for the "place all penguins" functionality
 We do not have this.
- the "loop till final game state"  function
https://github.ccs.neu.edu/CS4500-F20/bigsandy/blob/9b1e1a15623f75a3e87c7e076d7aad0cb5704503/Fish/Admin/referee.py#L57
- this function must initialize the game tree for the players that survived the start-up phase
In our interpretation.  Players are given the gamestate, instead of the gametree.  This is where they are given the final state.
https://github.ccs.neu.edu/CS4500-F20/bigsandy/blob/9b1e1a15623f75a3e87c7e076d7aad0cb5704503/Fish/Admin/referee.py#L61
- a unit test for the "loop till final game state"  function
https://github.ccs.neu.edu/CS4500-F20/bigsandy/blob/9b1e1a15623f75a3e87c7e076d7aad0cb5704503/Fish/Common/Tests/test_referee.py#L95

- the "one-round loop" function
This function is a part of the running of the game.

- a unit test for the "one-round loop" function
We do not have a test for this because it is not a stand alone function

- the "one-turn" per player function
https://github.ccs.neu.edu/CS4500-F20/bigsandy/blob/9b1e1a15623f75a3e87c7e076d7aad0cb5704503/Fish/Admin/referee.py#L93

- a unit test for the "one-turn per player" function with a well-behaved player
https://github.ccs.neu.edu/CS4500-F20/bigsandy/blob/9b1e1a15623f75a3e87c7e076d7aad0cb5704503/Fish/Common/Tests/test_referee.py#L159

- a unit test for the "one-turn" function with a cheating player
https://github.ccs.neu.edu/CS4500-F20/bigsandy/blob/9b1e1a15623f75a3e87c7e076d7aad0cb5704503/Fish/Common/Tests/test_referee.py#L133

- a unit test for the "one-turn" function with an failing player
I'm not sure what the difference between a cheating and a failing player is but we treat them the same.
https://github.ccs.neu.edu/CS4500-F20/bigsandy/blob/9b1e1a15623f75a3e87c7e076d7aad0cb5704503/Fish/Common/Tests/test_referee.py#L133
- for documenting which abnormal conditions the referee addresses
https://github.ccs.neu.edu/CS4500-F20/bigsandy/blob/9b1e1a15623f75a3e87c7e076d7aad0cb5704503/Fish/Admin/referee.py#L7

- the place where the referee re-initializes the game tree when a player is kicked out for cheating and/or failing
https://github.ccs.neu.edu/CS4500-F20/bigsandy/blob/9b1e1a15623f75a3e87c7e076d7aad0cb5704503/Fish/Admin/referee.py#L107


**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**

  WARNING: all perma-links must point to your commit "9b1e1a15623f75a3e87c7e076d7aad0cb5704503".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/bigsandy/tree/9b1e1a15623f75a3e87c7e076d7aad0cb5704503/Fish>
