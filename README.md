# Tiny-Rogue
A simple rogue-like game implemented in python.

ASCII Legend:
'#': wall
'O': player
'X': monster


Dungeon Layout:
- The dungeon is on a 8x8 grid.
- The dungeon's walls are randomly 

Game Start:
- The player (O) is randomly spwaned into a dungeon corner
- Monsters (X) are spanwed in the other 3 corners of the dungeon 

Game Turn:
-Player moves to an adjacent tile then all monsters move toward player

Combat:
- The player kills monsters by moving onto their square during their turn
- The monster kills the player by moving onto their square during their turn

Game Mechanics:
- Monsters always move toward the player using a shortest path algorithm
- Each monster has a 20% chance of not moving during their turn
- On every third turn the game attempts to spawn a new monster in the dungeon
	-Random Spawning does not occur if square is already occupied.
-If the player kills all monsters, they advance to next level and monsters spawn in corners

Scoring:
- The total number of monsters killed is tallied
- The player advances to the next level when all monsters in dungeon are slain

Win Condition:
The player continues to play the game until they are killed

Player Movement:
-Player can move in cardinal and ordinal directions.
-Players cannot move into squares with a wall on it
-Players cannot move between diagonal walls

w: Move up
a: Move left
s: Move down
d: Move right
wa: move up-left
wd: move up-right
sa: move down-left
sd: move down-right