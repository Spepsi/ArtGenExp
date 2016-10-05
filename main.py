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

idx = 0

debug = True

sizeX = 80
sizeY = 80
world = World(sizeX,sizeY)




if __name__=='__main__':
	print "hello gilles!"
	interface.main(world)

