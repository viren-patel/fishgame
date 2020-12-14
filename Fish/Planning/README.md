# Fish

### Prerequisites

* Python 3
* Tkinter



## Running Tests
Run 'python -m unittest' in the Fish/Common directory to run the unit tests.
Use the test harness xboard with the command "cat [test-file] | python3 xboard"
Use the test harness xstate with the command "cat [test-file] | python3 xstate"
Use the test harness xtree with the command "cat [test-file] | python3 xtree"
Use the test harness xstrategy with the command "cat [test-file] | python3 xstrategy"
## Directories and Files
    * 3 - Directory containing the test harness for the board.
      * xboard - test harness for the board object within /Fish/Common/board.py
      * Tests - Directory containing example tests and outputs for xboard
    * 4 - Directory containing the test harness for the state.
      * xstate - test harness for the state object within /Fish/Common/state.py
      * Tests - Directory containing example tests and outputs for xstate    
    * 5
      * xtree - test harness for the tree obejct within /Fish/Common/game_tree.py
      * Tests - Directory containing example tests and outputs for xtree
    * 6
      * xstrategy - test harness for the strategy functions within /Fish/Common/strategy.py
      * Tests - Directory containing example tests and outputs for xstrategy
    * Fish
      * Admin - Directory for Administrative classes such as referees
        * referee.py - Contains the prototype for a referee.  this referee is subject to change as the project adds functionality for remote players.
        * manager_interface.py - Contains an abstract class for the building of a tournament manager.
      * Common - Directory for game related classes such as the board and state
        * board.py - Contains representation for a board, and tile as well as methods to visually render both
        * game_tree.py - contains representation of a node of a game tree.  Uses classes contained in board.py and state.py
        * player.py - contains a representation of a player
        * player_interface.py - contains an abstract class for the building of a player AI     
        * state.py - Contains representation for the state of the game, as well as a method to visually render it.  Uses classes contained in board.py'
        * utils.py - contains a Function for parsing Jsons
        * Tests - Directory containing tests for the various data representations in this folder.
      * Planning - Directory for the planning and design of the Project, contains intiial designs as well as this README
      * Player - Directory for player AIs
        * strategy.py - Contains functions for a basic player strategy where moves are decided by a minmax search.
        * player.py - Contains a simple Example playerAI





## Authors

* **Michael Tang
* **Nicholas Ding
