# Server Architecture

The server architecture for the game is contained in [server.py](server.py).

## FishClient

Represents the server-side representation of an individual client, and manages the connection with that client. Handles sending various commands to a client and receiving the response. When a player is removed from the game, their socket should be closed.

## FishServer

Represents the server itself that runs the tournament. Does not spawn new threads itself, but the [tournament manager](../Admin/manager.py) may. The tournament handles timeouts, but FishServer handles the waiting period between classes. Does not run a tournament if too many players fail to send a name before it starts or after two waiting periods with insufficient players, and proceeds to close the primary socket if so.

# Timeouts

New code for timeouts is located in [timeout.py](timeout.py). This code spawns new processes for time sensitive tasks and kills them if they exceed the timeout period, which is currently set to 1 second.

# Changes

- Tournament and Referee now use a timeout system for awaiting responses to the `start`, `playing-as`, `playing-with`, `setup`, `take-turn`, and `end` methods, and players that do not adhere to the time limit are disqualified.
- Referee now maintains a dict of players and the list of actions that have occurred since their last turn, which is cleared when a player is removed or the corresponding player takes their turn. This is used as an argument to `take-turn`.
