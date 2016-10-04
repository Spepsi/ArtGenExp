import numpy as np 
import pandas as pd
import pygame as pg

from world import World
from human import Human
import interface




nb_cells_visible = 80
nb_stats = 4
nb_ressources = 6
proba_mutation = 0.02
shape_dna = (4,nb_cells_visible*nb_ressources+nb_stats)

sizeX = 100
sizeY = 100

nb_humans_start = 100

proba_food = 0.05
proba_water = 0.05
proba_rock = 0.05

idx = 0L

debug = True


world = World(100,100)








if __name__=='__main__':
	print "hello gilles!"
	interface.main(world)

