import numpy as np
from human import Human


sizeX = 100
sizeY = 100

nb_humans_start = 100

proba_food = 0.05
proba_water = 0.05
proba_rock = 0.05

debug = True

PVMAX = 0
STAMINA = 1
SIGHT = 2
PV = 3
class World:
	def __init__(self,sizeX,sizeY):
		self.idx = 0L
		self.sizeX = sizeX
		self.sizeY = sizeY
		self.board = {
						'humans'  : np.zeros((sizeX,sizeY)),
						'food': np.zeros((sizeX,sizeY)),
						'pheromones' : np.zeros((sizeX,sizeY)),
						'rock': np.zeros((sizeX,sizeY)),
						'water': np.zeros((sizeX,sizeY))

					}
		

		# Generate random initialization
		# Humans
		self.humans = []
		for i in range(nb_humans_start):
			self.create_human(Human(self,self.idx))
			self.idx+=1

		# water
		for i in range(sizeX):
			for j in range(sizeY):
				if np.random.random()<proba_rock:
					self.board['rock'][i,j] = 1
				if np.random.random()<proba_water:
					self.board['water'][i,j] = 1


		# food
		# rock

	def create_human(self,human):
		self.humans.append(human)
		print 'create : '+str(human.x)+' '+str(human.y)
		self.board['humans'][int(human.x),int(human.y)]+=1


	def do(self):
	
		if debug:
			print str(len(self.humans))+' '+str(np.sum(self.board['humans']))
		# Create food
		for i in range(self.sizeX):
			for j in range(self.sizeY):
				if np.random.random()<proba_food:
					self.board['food'][i,j] += 1
		to_remove = []
		for idx,h in enumerate(self.humans):
			h.stats[PV]-=1
			if h.stats[PV]<=0:
				to_remove.append(h)

			else:
				h.do()

		for h in to_remove:
			self.humans.remove(h)
			self.board['humans'][h.x,h.y]-=1

		for i in range(self.sizeX):
			for j in range(self.sizeY):
				self.board['pheromones'][i,j] = np.max(0,self.board['pheromones'][i,j]-1)

