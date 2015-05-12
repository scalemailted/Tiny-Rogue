# Tiny-Rogue
A simple rogue-like game implemented in python.

#### ASCII Legend:
&nbsp;&nbsp;&nbsp;&nbsp;**'#':** wall <br />
&nbsp;&nbsp;&nbsp;&nbsp;**'O':** player <br />
&nbsp;&nbsp;&nbsp;&nbsp;**'X':** monster <br />


#### Dungeon Layout:
- The dungeon is on a 8x8 grid.
- The dungeon's walls are randomly 

#### Game Start:
- The player *(O)* is randomly spwaned into a dungeon corner
- Monsters *(X)* are spanwed in the other 3 corners of the dungeon 

#### Game Turn:
- This is a turn-based game.
- Player moves to an adjacent tile then all monsters move toward player

#### Combat:
- The player kills monsters by moving onto their square during their turn
- The monster kills the player by moving onto their square during their turn

#### Game Mechanics:
- Monsters always move toward the player using a shortest path algorithm
- Each monster has a 20% chance of not moving during their turn
- On every third turn the game attempts to spawn a new monster in the dungeon
	+ Random Spawning does not occur if square is already occupied.
-If the player kills all monsters, they advance to next level and monsters spawn in corners

#### Scoring:
- The total number of monsters killed is tallied
- The player advances to the next level when all monsters in dungeon are slain

#### Win Condition:
The player continues to play the game until they are killed

#### Player Movement:
- Player can move in cardinal and ordinal directions.
- Players cannot move into squares with a wall on it
- Players cannot move between diagonal walls
- Players can take null actions by just pressing *"enter"*

#### Keyboard Controls:
&nbsp;&nbsp;&nbsp;&nbsp;**w:** move up <br />
&nbsp;&nbsp;&nbsp;&nbsp;**a:** move left <br />
&nbsp;&nbsp;&nbsp;&nbsp;**s:** move down <br />
&nbsp;&nbsp;&nbsp;&nbsp;**d:** move right <br />
&nbsp;&nbsp;&nbsp;&nbsp;**wa:** move up-left <br />
&nbsp;&nbsp;&nbsp;&nbsp;**wd:** move up-right <br />
&nbsp;&nbsp;&nbsp;&nbsp;**sa:** move down-left <br />
&nbsp;&nbsp;&nbsp;&nbsp;**sd:** move down-right <br />
&nbsp;&nbsp;&nbsp;&nbsp;**enter:** input command <br />