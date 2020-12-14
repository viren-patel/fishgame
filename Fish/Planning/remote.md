# Remote Collaboration Protocol

## Interaction Diagram:
Sign up Phase:
Remote Player                                   Connection Server                                   Administrator
    |   ------------ Connection Request --------->      |                                               |
    |   <------- Connection Acknowledgement -----       |                                               |
    |                                                   |  <--------------- Open Signup Message ------- |
    |   < Open Sign Up Message ------------------       |                                               |
    |   ------------- Sign Up Request ----------->      |                                               |
    |                                                   | --------------- Sign Up Notification------->  |
    |                                                   | <-------------- Sign Up Acknowledgement-----  |
    |   <------------Sign Up Acknowledgement -----      |                                               |

Gameplay:
Remote Player                                   Connection Server                                   Administrator
    |                                                   |  <----------- Tournament Start -------------  | 
    | <------------ Tournament Start -----------------  |                                               |
    |                                                   |  <------------ Action Request --------------  |
    | <-------------- Action Request -----------------  |                                               |
    | -------------------Send Action ---------------->  |                                               |
    |                                                   | ----------------- Send Action ------------->  |
    |                                                   | <--------- Return Whether Valid Action -----  |     (This Handles Telling Cheaters they have been kicked)
    | <---------- Return Whether Valid Action -------   |                                               |
    |                                                   | <-----------------Send Gamestate -----------  |     (This occurs at the beginning of the game, 
    | <-----------------Send Gamestate --------------   |                                               |     and after any move has been played)


Game End:
Remote Player                                   Connection Server                                   Administrator
    |                                                   | <------------- Game Loss message -----------  |     (This is sent from the tournament to losing players)
    | <----------------- Game Loss Message -----------  |                                               |
    |                                                   | <------------- Game Win Message ------------  |     (This is sent from the tournament to winning players)  
    | <------------- Game Win Message ----------------  |                                               |
    | -------------- Game Win Ack ------------------->  |                                               |     (Only Winning players send this,
    |                                                   | ----------------- Game Win Ack ------------>  |      if they do not they are considered losers)
    |                                                   |                                               |
    |                                                   | <-------------- Tournament Win Message ----   |     (This is sent from the tournament to winning players,
    | <-------------- Tournament Win Message ---------  |                                               |      after the tournament has ended)
    | --------------- Tournament Win Ack ------------>  |                                               |     (Only Winning players send this,
    |                                                   | ------------ Tournament Win Ack ----------->  |      if they do not they are considered losers)
    |                                                   |                                               |
    |                                                   | <--------------- Prize ---------------------  |     (This is sent from the tournament to winning players,
    | <--------------- Prize -------------------------  |                                               |      after their win has been acknowledged)
    |                                                   |                                               |
    |                                                   | <--------- Tournament Over Message---------   |     (Tell Players that the server is dropping the connection)
    | <---------- Disconnection Notification --------   |                                               |


## Logical Interactions

### Connection Request:
- Sent by the remote Player to request a connection to the server
- Server sends back a message acknowledging that the connection was successful

### Open Sign Up Message:
- First signaled by the tournament manager to tell the connection server that the sign up period has begun
- The server sends a message to the remove players to tell them that they can now sign up

### Sign Up Request:
- Sent by a remote player to ask to be signed up for the tournament (includes the payment for entering the tournament)
- The connection server signals to the Tournament manager that a new player has signed up
- Connection server sends an acknologement to the player telling them that they have successfully signed up for the tournament
- Example:
```json
{
    "type": "sign-up",
    "data": {
        "payment": {//payment information
        },
        "age": 0 //int representing the player's age
    }
}
{
    "type": "sign-up",
    "data": "ack"
}
```

### Tournament Start:
- The Tournament Manager signals to the Connection Server that the sign-up period is over and the tournament is starting
- The Connection Server sends a message to the players that have successfully signed up that the tournament is starting
```json
{
    "type": "tournament-start",
    "data": null
}
```

### Action Request:
- The Tournament Manager requests an action from the Connection Server for the player whose turn it is
- The Connection Server sends a message to that player requesting an action
```json
{
    "type": "action",
    "data": {
        "type": "placement|move" //could be either "placement" or "move"
    }
}
```

### Action Message:
- Sent by the remove player to the Connection Server representing a valid Action for the current game
- The Connection propogates this data to the Tournament Manager
```json
{
    "type": "action",
    "data": {
        "type": "placement|move", //could be either "placement" or "move",
        "action": [[]] //Could either be a pair of two ints representing a placement, a pair of pairs of two ints representing a move
    }
}
``` 
### Invalid Action:
- The Tournament Manager would signal to the Connection Server that a specific player's action was invalid or they cheated
- The Connection Server sends an Invalid Action message to the player which lets them know that they have been kicked
```json
{
    "type": "invalid-action",
    "data": [[]] //contains the bad action
}
```

### Gamestate Update:
- Contains all of the data necessary to represent the current Gamestate
- The Tournament Manager signals to the Connection Server to send a specific gamestate to the players for that game
- The Connection Server sends a Gamestate update message to the players of that game
- The "data" field of the dictionary is of type State which has been used for integration testing 
```json
{
    "type": "state",
    "data": {
        //State
    }
}
```

### Game Loss Message:
- The Tournament Manager sends a list of players that have lost the round and will not continue in the tournament
- The Connection Server sends a Game Loss message to the losing players
```json
{
    "type": "game-lost",
    "data": null
}
```

### Game Won Message:
- The Tournament Manager sends a list of players that have won the round and will continue in the tournament
- The Connection Server sends a Game Loss message to the winning players
- The player must send an acknologement back or else they are considered losers

```json
{ // Sent by the server
    "type": "game-won",
    "data": null
}

{ //Sent by the player
    "type": "ack",
    "data": null
}
```

### Tournament Won Message:
- The Tournament Manager sends a list of player(s) that have won the entire tournament to the Connection Server
- The Conneciton Server sends a Tournament Won Message to the player(s) that have won
- The player(s) send an acknologement back to the Connection Server
```json
{ //Sent by the server
    "type": "tournament-won",
    "data": null
}

{ // Sent by the winning player(s)
    "type": "ack",
    "data": null
}
```

### Prize
- Sent by the Tournament Manager to the Connection Server, which propogates prize information to the tournament winner(s)
```json
{
    "type": "prize",
    "data": {
        //prize information
    }
}
```

### Tournament Over / Disconnect
- The Tournament Manager signals that the tournament is over to the Connection Server
- The Connection Server sends a disconnect message to all remaining remote players and disconnects
```json
{
    "type": "disconnect",
    "data": null
}
```