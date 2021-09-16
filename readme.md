## CLI_Tic_Tac_Toe
A command line Tic_Tac_Toe game using python.

### Modules
#### game.py
Provide methods for:
* board rendering
* making moves
* game status checking and updating
* AI game solver

#### play.py
Provide command line interface for player to interact with the game.


### AI design
#### Easy
Make a random valid move

#### Medium
Evaluate if a move resulting an immediate win or immediate lose if the opponent makes the move.
If there are immediate winning moves, choose a random winning move.
After that, if there are immediate losing moves, choose one from them.
If there are no such moves, make a random valid move.

#### Hard
Use min-max algorithm, will choose the first valid move that has the highest score.

