import numpy as np

class Grid:
    """A grid Object containing a single Tic Tac Toe Grid"""
    __grid_play = np.zeros((3,3),int)
    __winner = None
    
    def __init__(self):
	self.__grid_play = np.zeros((3,3),int)
    
    def __str__(self):
	return str(self.__grid_play)
    
    def __test_winner(self,val1,val2):
	"""Test if a sum represent the amount of point a winner.
	If a winner is found, his name is stocked in self.__winner, True is returned.
	Else False is returned."""
	#Player1 play with 1. The sum of a line is 3.
	if val1==3 or val2==3:
	    self.__winner="player1"
	    return True
	#Player1 play with 4. The sum of a line is 12.
	elif val1==12 or val2==12:
	    self.__winner="player2"
	    return True
	return False
    
    
    def search_winner(self):
	"""Look for a winner in the matrix and return True if it match."""
	diag1=0
	diag2=0
	full=True
	for i in [0,1,2]:
	    line = self.__grid_play[i,:]
	    col = self.__grid_play[:,i]
	    if self.__test_winner(np.sum(line),np.sum(col)):
		return True
	    diag1+=self.__grid_play[i][i]
	    diag2+=self.__grid_play[i][2-i]
	    if full:
		for j in [0,1,2]:
		    if not self.__grid_play[i][j]:
			full=False
	if self.__test_winner(diag1,diag2):
	    return True
	if full:
	    self.__winner="null"
	    return True
	return False
    
    
    def set_in_grid(self,player,x,y):
	"""Add an element in the matrix game if the cell is free and return
	a tuple containing (True,x,y).
	If the cell is not empty, return (False,x,y)"""
	if self.__winner:
	    return False,x,y
	if self.__grid_play[x,y]:
	    return False,x,y
	if player==1:
	    self.__grid_play[x,y]=1
	else:
	    self.__grid_play[x,y]=4
	self.search_winner()
	return True,x,y
    
    
    def get_winner(self):
	"""Return the winner or None"""
	return self.__winner
    
    def print_grid(self):
	"""Print the game matrix."""
	print self.__grid_play
    
    def cell_status(self,x,y):
	"""Return the status of the cell.
	If empty : False
	Else : True"""
	if not self.__grid_play[x,y]:
	  #rien dans la case
	  return False
	#case occupee
	return True
    
    def get_grid(self):
	"""Return the matrix."""
	return self.__grid_play
    
    def reboot_grid(self):
	"""reinitialze the grid"""
	self.__grid_play = np.zeros((3,3),int)



class Master_Grid(Grid):
    """A Master_Grid object containing the global results Grid and
    a Grid of nine standard Tic Tac Toe Grid"""
    
    def __init__(self):
	self.__inner_list=np.array([[Grid(),Grid(),Grid()],
		                    [Grid(),Grid(),Grid()],
		                    [Grid(),Grid(),Grid()]])
    
    def __str__(self):
	ret=""
	for i in range(9):
	    for j in range(9):
		ret+=self.int2char(self.__inner_list[i/3,j/3].get_grid()[i%3,j%3])+" "
		if j==2 or j==5:
		    ret+="| "
	    ret+="    "
	    
	    # Create the Master Grid with inner Grids and 
	    for j in range(9):
		if i%3==0 or i%3==2 or j%3!=1:
		    ret+="  "
		else:
		    w=self.__inner_list[i/3,j/3].get_winner()
		    if w:
			if w=="player1":
			    ret+="O "
			elif w=="player2":
			    ret+="X "
			else:
			    ret+="n "
		    else:
			ret+="  "
		if j==2 or j==5:
		    ret+="| "
	    
	    # Create horizontal lines between inner Grids 
	    if i==2 or i==5:
		ret+="\n"
		for j in range(18):
		    ret+="--"
		    if j==2 or j==5 or j==11 or j==14:
			ret+="+-"
		    if j==8:
			ret+="    "
	    ret+="\n"
	return ret+"\n"
    
    @staticmethod
    def int2char(c):
	"""Convert 1 to O, 4 to X or 0 to a blank character"""
	return {1:"O",4:"X",0:" "}[c]
    
    def set_in_inner_grid(self,player,master_X,master_Y,x,y):
	"""Set a value in the selected standard Tic Tac Toe Grid an return
	a tuple containing (True,x,y).
	If the cell is not empty, return (False,x,y)"""
	return_tuple=self.__inner_list[master_X,master_Y].set_in_grid(player,x,y)
	if self.__inner_list[master_X,master_Y].get_winner():
	    self.set_in_grid(player,master_X,master_Y)
	return return_tuple
    
    def inner_grid_status(self,master_X,master_Y):
	"""Try to hange the status of a case of the master grid.
	If there is a winner in the inner grid, the value is set
	in self.__grid_play"""
	status=self.__inner_list[master_X,master_Y].search_winner()
	if status:
	    winner=self.__inner_list[master_X,master_Y].get_winner()
	    if winner=="player1":
		self.set_in_grid(1,master_X,master_Y)
	    else:
		self.set_in_grid(2,master_X,master_Y)
	    return True
	return False
    
    def get_inner_grid(self, x, y):
	"""Return the selected standard Tic Tac Toe Grid."""
	return self.__inner_list[x,y]

    def reboot_master_grid(self):
	"""reinitialze the master grid"""
	self.reboot_grid()
	self.__inner_list=np.array([[Grid(),Grid(),Grid()],
		                    [Grid(),Grid(),Grid()],
		                    [Grid(),Grid(),Grid()]])
