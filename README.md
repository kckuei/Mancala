# Mancala
Toy command line Mancala board game implemented with python. 

👉[Live demo](https://replit.com/@KevinKuei/Mancala-Game#main.py)👈

## Rules
* Read about the official rules for the game [here](https://www.officialgamerules.org/mancala).

## Implementation Notes

### Classes
The game is implemented with 4 basic classes as follows:
* Mancala - Mancala class representing the game as played.
* Player - Player class representing each of the players.
* Board - Board class representing the Mancala board.
* Container - Container class representing seed pits/stores.

### Design
The smallest abstraction is a `Container` class that is used to represent seed 'pits' and 'stores'. Containers can store seeds, and have attribute pointers to the next pits/store in line (similar to nodes in a tree). Containers can also have 'adjacent' attribute pointers (in the case that they are pits), to select opposing player pits. This is useful for implementing special game rules such as when a player lands on one of their empty pits with their last seed in a given turn.

Pits and stores are strung together through their pointers to create a closed-circuit, which emulates the counter-clockwise navigation and traversal of the physical Mancala board.

The `Board` class is subsequently represented as a collection of Container objects. Given any one of the pointers for a pit, the board can be traversed, and seeds distributed amongst them. The pointers for the pits/stores for each player are collected/grouped as an attribute in the Board class to create a common access interface. This makes manipulation of seed values, in conjunction with the pointers, trivial for tasks such as distributing and transfering seeds between other pits and stores.

Players are presented by a trivial `Player` class with their names.

The `Mancala` class representing the game as played, builds on the other class abstractions. Each Mancala object has two Players, and a Board.


## Example Gameplay
