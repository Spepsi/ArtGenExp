import numpy as np 
import pandas as pd
import pygame as pg


nb_cells_visible = 80
nb_stats = 4
nb_ressources = 6
proba_mutation = 0.02
shape_dna = (2,nb_cells_visible*nb_ressources+nb_stats)

sizeX = 100
sizeY = 100
world = World(sizeX,sizeY)


def merge_dna(parent1,parent2):
	dna = np.zeros(parent1.dna.shape)
	stats = np.zeros(parent1.stats.shape)

	for i,array in enumerate(parent1.dna):
		for j,_ in enumerate(array):
			if np.random.random()<proba_mutation:
				dna[i,j] = np.random.randn()
			else:
				dna[i,j] = (parent1.dna[i,j] if np.random.random()>0.5   else parent2.dna[i,j])

	for j,_ in enumerate(parent1.stats):
		if np.random.random()<proba_mutation:
			stats[j] = np.ranom.randn()
		else:
			stats[j] =  (parent1.stats[j]  if np.random.random()>0.5 else parent2.stats[j])
	# Mutation !!!!
	return dna,stats


class Human:
	def __init__(self,parent1=None,parent2=None):

		self.dna = np.zeros(shape_dna)
		self.stats = np.zeros(nb_stats-1)

		if parent1==None and parent2==None:
			self.dna = np.random.randn(*shape_dna)
			self.stats = np.random.randn(nb_stats)
			self.x = sizeX/2
			self.y = sizeY/2

		else:
			self.dna,self.stats = merge_dna(parent1,parent2)
			self.x = parent1.x
			self.y = parent1.y

	def do(self):
		# TODO : remove random sensitivy
		output = np.dot(self.dna,np.random.random(self.dna.shape[1]))
		direction = np.argmax(np.abs(output[0]),np.abs(output[1]))
		if np.abs(output[0])>np.abs(output[1]):
			self.x = self.x + (np.sign(output[0]))
		else:
			self.y = self.y + (np.sign(output[1]))



class World:
	def __init__(self,sizeX,sizeY):
		self.sizeX = sizeX
		self.sizeY = sizeY
		self.board = {
						'humans'  : np.zeros((self.sizeX,self.sizeY)),
						'food': np.zeros((self.sizeX,self.sizeY)),
						'pheromones' : np.zeros((self.sizeX,self.sizeY)),
						'rock': np.zeros((self.sizeX,self.sizeY)),
						'water': np.zeros((self.sizeX,self.sizeY))

					}
		self.humans =[]

		# Generate random
	def do(self):
		for h in self.humans:
			h.do()
		for i in range(self.sizeX):
			for j in range(self.sizeY):
				self.board['pheromones'][i,j] = np.max(0,self.board['pheromones'][i,j]-1)
				self.board['food'][i,j] = np.max(0,self.board['food'][i,j]-self.board['humans'][i,j])




if __name__=='__main__':
	print "hello gilles!"

	Gilles = Human()
	Bouard = Human()
	GillesBouard = Human(Gilles,Bouard)

	print Gilles.dna
	print Bouard.dna
	print GillesBouard.dna

