# -*- coding: utf-8 -*-


import random as r
import numpy as nu

class Player:
    """Abstract Class to define a player"""
    __player_type=None
    __name=None
    __grid=None
    
    def __init__(self):
	self.__name=None
	self.__player_num=None
	self.__player_type=None
    
    def __str__(self):
	return self.__name
    
    def set_player_type(self,player_type):
	"""add a type to the Player object"""
	self.__player_type=player_type
    
    def set_player_name(self,name):
	"""add a name to the Player object"""
	self.__name=name
    
    def set_player_num(self,num):
	"""add a number to the Player object"""
	self.__num=num
    
    def get_type(self):
	"""return the Player type"""
	return self.__player_type
    
    def get_name(self):
	"""return the Player name"""
	return self.__name
    
    def get_num(self):
	"""return the Player number"""
	return self.__num
    
    def reflexion(self):
	"""method to return coordonate of the next move"""
	pass
    
    def set_grid(self, grid):
      """add a grid to the Player object"""
      self.__grid=grid
    
    def get_grid(self):
      """return the grid from the Player"""
      return self.__grid


class Human(Player):
    """Define a Human player herited from Player."""
    def __init__(self, name="jojo le joueur", num=0):
	self.set_player_type("human")
	self.set_player_name(name)
	self.set_player_num(num)
    
    def reflexion(self, grid,unuse):
	"""Ask coordonate to the player to the next move and return them.
	Usefull with terminal game."""
	self.set_grid(grid)
	while True:
	    try:
		x=input("valeur de X : ")
		break
	    except:
		print "Again"
	while True:
	    try:
		y=input("valeur de Y : ")
		break
	    except:
		print "Again"
	return x,y


class IA(Player):
    """Define an IA player herited from Player"""
    def __init__(self,name="jojo l'IA",num=0):
	self.set_player_type("IA")
	self.set_player_name(name)
	self.set_player_num(num)
	self.__zone=None,None
    
    def reflexion(self, grid, level,actual):
	"""Generate coordonate for the next move.
	level=0 : Random coordonate
	level=1 : Best coordonate to win or block the other player
	          with a probability of random move"""
	if level==0:
	    return r.randint(0,8),r.randint(0,8)
	elif level==1:
	    if actual[0]==None:
		actual=self.random_free_cell(grid.get_grid())
	    x,y=self.define_best_cells(grid.get_inner_grid(actual[0],
				       actual[1]).get_grid(), self.get_num())
	    x+=(3*actual[0])
	    y+=(3*actual[1])
	    return x,y
	else:
	    return r.randint(0,8),r.randint(0,8)
    
    def define_best_cells(self,grid, motif):
	"""Find a cell to play with a probability of random play and return it.
	grid is a matrix
	motif=1 or 2"""
	#listes de lignes à compléter
	player1=[]
	player2=[]
	#score des diagonales
	sumD1=0
	sumD2=0
	#recherches des lignes de deux éléments
	for i in [0,1,2]:
	    if nu.sum(grid[i,:])==2:
		player1.append("l"+str(i))
	    elif nu.sum(grid[i,:])==8:
		player2.append("l"+str(i))
	    if nu.sum(grid[:,i])==2:
		player1.append("c"+str(i))
	    elif nu.sum(grid[:,i])==8:
		player2.append("c"+str(i))
	    sumD1+=grid[i,i]
	    sumD2+=grid[i,2-i]
	if sumD1==2:
	    player1.append("d1")
	elif sumD1==8:
	    player2.append("d1")
	if sumD2==2:
	    player1.append("d2")
	elif sumD2==8:
	    player2.append("d2")
	l1=len(player1)
	l2=len(player2)
	#probabilité de ne pas jouer logiquement
	r1=r.randint(0,10)
	r2=r.randint(0,10)
	#réccupération des coordonnées
	if motif==1 :
	    if l1>0 and r1<9:
		return self.free_cell(grid,player1)
	    if l2>0 and r2<9:
		return self.free_cell(grid,player2)
	else:
	    if l2>0 and r1<9:
		return self.free_cell(grid,player2)
	    if l1>0 and r2<9:
		return self.free_cell(grid,player1)
	return self.random_free_cell(grid)
    
    
    @staticmethod
    def free_cell(grid, liste):
	"""Find a free cell in a line or a colonne to complete.
	Or find a random free cell.
	Return the coordonate."""
	#élément aléatoire dans la liste de lignes à compléter
	l=liste[r.choice(range(len(liste)))]
	for i in [0,1,2]:
	    if l[0]=="c":
		if not grid[i,int(l[1])]:
		    return i,int(l[1])
	    elif l[0]=="l":
		if not grid[int(l[1]),i]:
		    return int(l[1]),i
	    elif l=="d1":
		if not grid[i,i]:
		    return i,i
	    else:
		if not grid[i,2-i]:
		    return i,2-i
    
    
    @staticmethod
    def random_free_cell(grid):
	"""Find randomly a free cell in the grid."""
	#liste de cases vides
	list_cells=[]
	for i in [0,1,2]:
	    for j in [0,1,2]:
		if not grid[i,j]:
		    list_cells.append((i,j))
	return r.choice(list_cells)
      