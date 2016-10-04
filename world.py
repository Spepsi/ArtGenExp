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
AGE = 4

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
		for i in range(1,sizeX-1):
			for j in range(1,sizeY-1):
				if np.random.random()<proba_rock:
					self.board['rock'][i,j] = 1
				if np.random.random()<proba_water:
					self.board['water'][i,j] = 1
		for i in range(sizeX):
			self.board['water'][i,0] = 1
			self.board['water'][i,sizeY-1] = 1
		for j in range(sizeY):
			self.board['water'][0,j] = 1
			self.board['water'][sizeX-1,j] = 1

		# food
		# rock

	def create_human(self,human):
		self.humans.append(human)	
		self.board['humans'][int(human.x),int(human.y)]+=1


	def do(self):
	
		if debug:
			print str(len(self.humans))+' '+str(np.sum(self.board['humans']))
		# Create food
		proba_new_food = 0.5
		if np.random.random()<proba_new_food:
			i = np.random.randint(1,sizeX-1)
			j = np.random.randint(1,sizeY-1)
			if self.is_food_possible(i,j):
				self.board["food"][i,j]+=1
		# Propagate food
		proba_food_propagate = 0.2
		proba_food_growth = 0.2
		for i in range(1,self.sizeX-1):
			for j in range(1,self.sizeY-1):
				if self.board["food"][i,j]>0:
					if np.random.random()<proba_food_growth:
						self.board["food"][i,j]+=1
				elif self.is_food_possible(i,j):
					p = 0
					for i2,j2 in [[i-1,j],[i+1,j],[i,j-1],[i,j+1]]:
						if self.board["food"][i2,j2]>0:
							p += proba_food_propagate
					if np.random.random()<p:
						self.board["food"][i,j] += 1
		to_remove = []
		for idx,h in enumerate(self.humans):
			h.stats[PV]-=1
			if h.stats[PV]<=0 or self.board['water'][h.x,h.y]>0:
				to_remove.append(h)

			else:
				h.do()
		print 'dying : '+str(len(to_remove))
		for h in to_remove:
			self.humans.remove(h)
			self.board['humans'][h.x,h.y]-=1

		for i in range(self.sizeX):
			for j in range(self.sizeY):
				self.board['pheromones'][i,j] = np.max(0,self.board['pheromones'][i,j]-1)

	def is_food_possible(self,i,j):
		return self.board["rock"][i,j]==0 and self.board["water"][i,j]==0

