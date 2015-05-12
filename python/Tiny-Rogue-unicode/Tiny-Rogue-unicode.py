
import sys
import random
import time



#######################################################################
###  CLASSES & FXNS
#######################################################################


class Room(object):
    #Constructor, setups an instance of room
    def __init__(self, row=8, col=8):
        self.row_size = row
        self.col_size = col
        self.grid = self.generate_grid()
        self.player_pos = self.rand_player_pos()
        self.level = 0
        self.kills = 0
        self.generate_npcs()
        #self.npc_pos = self.generate_npc_pos(self.player_pos)
    #Creates new random set of tiles for this room
    def generate_grid(self):
        grid = [['.']*self.col_size for i in range(self.row_size)]
        for i in range(self.row_size):
            for j in range(self.col_size):
                if random.randint(1, 4) == 1:
                    grid[i][j] = '#'                
        return grid
    #Creates random spawn points for pc
    def rand_player_pos(self):
        x,y = random.randint(0,1)*7, random.randint(0,1)*7
        self.grid[x][y] = 'O'
        return x,y
    #Set npc in opposite corner of pc
    #def generate_npc_pos(self,(x,y)):
    #    dx,dy = abs(x-7),abs(y-7)
    #    self.grid[dx][dy] = 'X'
    #    return dx, dy
    def generate_npcs(self):
        self.level+=1
        self.npcs = set()
        spawn_pts = {(0,0),(0,7),(7,0),(7,7)}
        for cell in spawn_pts:
            if self.player_pos != cell:
                dx,dy = cell
                self.grid[dx][dy] = 'X'
                self.npcs.add(cell)
    #Move player
    def move_player(self,(dx,dy)):
        x,y = self.player_pos
        if self.is_open_cell(dx,dy) and self.valid_diag_move((x,y),(dx,dy)):
            self.grid[x][y] = '.'
            self.grid[dx][dy] = 'O'
            self.player_pos = dx,dy
            if (dx,dy) in self.npcs:
                self.npcs.remove((dx,dy))
                self.kills+=1
    #Move npc
    def move_npc(self, (x,y),(dx,dy)):
        if self.is_open_cell(dx,dy) and (dx,dy) not in self.npcs:
            self.npcs.remove((x,y))
            self.grid[x][y] = '.'
            self.grid[dx][dy] = 'X'
            self.npcs.add((dx,dy))
    #Display the state of this room
    def display(self):
        print("\033[H\033[2J")
        sys.stdout.write('\x1b[7m \x1b[0m'*(self.col_size+2)) #Black Top Border
        sys.stdout.write('\n')
        for i in xrange(self.row_size):
            sys.stdout.write('\x1b[7m \x1b[0m') #Black Left Border
            for j in xrange(self.col_size):
                if self.grid[i][j] == '#':
                    sys.stdout.write('\x1b[7m \x1b[0m') #GREEN
                elif self.grid[i][j] == 'O':
                    sys.stdout.write('\x1b[1;32m'+u"\u263B"+'\x1b[0m') #YELLOW
                elif self.grid[i][j] == 'X':
                    sys.stdout.write('\x1b[1;31m'+u"\u2689"+'\x1b[0m') #RED
                else:
                    sys.stdout.write(u"\u00b7") #OFF
            sys.stdout.write('\x1b[7m \x1b[0m') #Black Right Border
            sys.stdout.write('\n')
        sys.stdout.write('\x1b[7m \x1b[0m'*(self.col_size+2)) #Black Bottom Border
        sys.stdout.write('\n')
    #Check if cell is in bounds and not a wall
    def is_open_cell(self,x,y):
        return 0<=x<self.row_size and 0<=y<self.col_size and self.grid[x][y] != '#'
    #Add new enemy
    def add_npc(self, (x,y)):
        if self.is_open_cell(x,y) and (x,y) not in self.npcs and (x,y) != self.player_pos and plot_shortest_path(self, (x,y)) != []:
            self.npcs.add((x,y))
            self.grid[x][y] = 'X'
            self.display()
    def valid_diag_move( self,(x,y),(dx,dy)):
        return (abs(dx-x) + abs(dy-y) != 2) or (self.is_open_cell(dx,y) or self.is_open_cell(x,dy))

        




def player_turn(room):
    global gameover
    row,col = room.player_pos
    adjacencies = {'W':(row-1,col),\
                   'A':(row,col-1),\
                   'S':(row+1,col),\
                   'D':(row,col+1),\
                   'WA':(row-1,col-1),\
                   'WD':(row-1,col+1),\
                   'SA':(row+1,col-1),\
                   'SD':(row+1,col+1)}

    user_input = raw_input().upper()

    if user_input in adjacencies.keys():
        room.move_player(adjacencies[user_input])
        gameover = is_gameover(room)
    #elif user_input == 'Q':
    #    gameover = True
    #else:
    #    print "Don't understand that key!"
    #    print "Use WASD to move or Q to quit"
    #    player_turn(room)



def npc_turn(room):
    npcs = [] + list(room.npcs)
    for npc in npcs:
        #print npcs
        path = plot_shortest_path(room, npc)
        if len(path) >1 and random.randint(1,5) != 1:
            room.move_npc(path[0],path[1])
        time.sleep(0.15)
        room.display()
        global gameover
        gameover = is_gameover(room)



def create_room():
    while (True): 
        room = Room()
        vaild_paths = []
        for npc in room.npcs:
            vaild_paths.append(plot_shortest_path(room, npc))
        if [] not in vaild_paths:
            break       
    return room

def is_gameover(room):
    x,y = room.player_pos
    return (x,y) in room.npcs and room.grid[x][y] == 'X'

def get_winner(room):
    if is_gameover(room):
        x,y = room.player_pos
        winner = "Player" if room.grid[x][y] == 'O' else "Computer"
        return winner



def plot_shortest_path(room, npc):
    #STARTING NODE
    source_node = npc
    #CONSTANTS
    INFINITY = float("inf")     #Infinity
    #GRAPH & WEIGHTS
    graph = create_graph(room)
    weights = {'#':INFINITY, '.':1,'O':1,'X':1}
    #INITIALIZE ALL WEIGHTS FROM SOURCE NODE'
    node_weights = {node: INFINITY for node in graph.keys()}
    node_weights[source_node] = 0
    #INITIALIZE EMPTY PATHS TO TARGET NODES
    node_paths = {node: [] for node in graph.keys()}
    node_paths[source_node] += [source_node]
    #INITIALIZE LIST OF ALL UNVISITED NODES
    unvisited_nodes = graph.keys()
    #DIJKSTRAS ALGORITHM
    while unvisited_nodes:
        source_node = sorted(unvisited_nodes, key= lambda x: node_weights[x]).pop(0)
        for target_node in graph[source_node]:
            init_weight = node_weights[target_node]
            this_weight = weights[room.grid[source_node[0]][source_node[1]]] + node_weights[source_node]
            if this_weight < init_weight:
                node_weights[target_node] = this_weight
                node_paths[target_node] = node_paths[source_node] + [target_node]
        unvisited_nodes.remove(source_node)
    #
    return node_paths[room.player_pos] 



def create_graph(room):
    graph = {(i,j):[] for j in range(8) for i in range(8)}
    for i,j in graph.keys():
        #Orthogonal 
        if room.is_open_cell(i-1, j): 
            graph[(i,j)].append((i-1,j))
        if room.is_open_cell(i, j-1):
            graph[(i,j)].append((i,j-1))
        if room.is_open_cell(i+1, j):
            graph[(i,j)].append((i+1,j))
        if room.is_open_cell(i, j+1):
            graph[(i,j)].append((i,j+1))
        #Diagonal
        if room.is_open_cell(i-1, j-1) and room.valid_diag_move((i,j),(i-1,j-1)):
            graph[(i,j)].append((i-1,j-1))
        if room.is_open_cell(i+1, j-1) and room.valid_diag_move((i,j),(i+1,j-1)):
            graph[(i,j)].append((i+1,j-1))
        if room.is_open_cell(i-1, j+1) and room.valid_diag_move((i,j),(i-1,j+1)):
            graph[(i,j)].append((i-1,j+1))
        if room.is_open_cell(i+1, j+1) and room.valid_diag_move((i,j),(i+1,j+1)):
            graph[(i,j)].append((i+1,j+1))
    return graph




room = create_room()
gameover = False
counter = 1
while not gameover:
    room.display()
    player_turn(room)
    room.display()
    if room.npcs:
        npc_turn(room)
    else:
        room.generate_npcs()
        couter = 1
    if counter % 3 == 0 :
        x,y = random.randint(0,7), random.randint(0,7)
        room.add_npc((x,y))
    room.display()
    counter+=1
   

print "Thanks for playing!"
if is_gameover(room):
    #print "the winner is: " + get_winner(room)
    print "You got to level " + str(room.level)
    print "You had " + str(room.kills) + " kills."


#if  __name__ =='__main__':main()





"""
def add_npc(self, (x,y)):
    if is_open_cell(x,y) and (x,y) not in npcs:
        self.npcs.add((x,y))


self.npc_qty = 1 #increase this when all killed 
self.npcs = set()
"""

#count hoe many they killed in game
#incrments npc_qty and generate new enemies
#win condition: for computer if player_pos in npcs and grid[i][j] == 'X'

