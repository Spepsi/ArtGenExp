import numpy as np
import random


nb_cells_visible = 80
nb_stats = 4
nb_ressources = 6
proba_mutation = 0.02
shape_dna = (4,nb_cells_visible*nb_ressources+nb_stats)
X = 0
Y = 1
EAT = 2
FUCK = 3

PVMAX = 0
STAMINA = 1
SIGHT = 2
PV = 3



debug = False


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
			if j==SIGHT:
				stats[j] = 4*np.random.random()
			if j==PVMAX:
				stats[j] = 100*np.random.random()
		else:
			stats[j] =  (parent1.stats[j]  if np.random.random()>0.5 else parent2.stats[j])

	stats[PV] = stats[PVMAX]
	# Mutation !!!!
	return dna,stats

class Human:
	def __init__(self,world,idx,parent1=None,parent2=None):
		self.world = world
		self.dna = np.zeros(shape_dna)
		self.stats = np.zeros(nb_stats-1)
		self.idx = idx
		

		if parent1==None and parent2==None:
			self.dna = np.random.randn(*shape_dna)
			self.stats = np.random.randn(nb_stats)
			self.x = self.world.sizeX/2
			self.y = self.world.sizeY/2

		else:
			self.dna,self.stats = merge_dna(parent1,parent2)
			self.x = parent1.x
			self.y = parent1.y

	def do(self):
		# TODO : remove random sensitivy
		if debug:
			'action for : '+str(self.idx)




		# Choose the action

		output = np.dot(self.dna,np.random.random(self.dna.shape[1]))
		action = np.argmax(np.abs(output))

		if action==X or action==Y:
			self.move(output)
		elif action==EAT:
			self.eat()
		elif action==FUCK:
			self.fuck()

		if debug:
			if action==X:
				print 'move X'
			if action == Y:
				print 'move Y'
			if action == EAT:
				print 'eat'
			if action == FUCK:
				print 'fuck'

	def move(self,output):
		self.world.board['humans'][self.x,self.y]-=1
		if np.abs(output[0])>np.abs(output[1]):
			
			self.x = self.x + (np.sign(output[0]))
		else:
			self.y = self.y + (np.sign(output[1]))
		self.world.board['humans'][self.x,self.y]+=1

	def fuck(self):
		# Get all the humans in the cell
		if self.world.board['humans'][self.x,self.y] > 1:
			# Find another human being
			humans = []
			for h in self.world.humans:
				if h.x==self.x and h.y == self.y and self.idx!=h.idx:
					humans.append(h)
			# Choose human at random
			partner = random.choice(humans)
			self.world.create_human(Human(self.world,self.world.idx,self,partner))
			self.world.idx += 1

	def eat(self):
		# Remove food from board
		if self.world.board['humans'][self.x,self.y] > 0:
			self.stats[PV] = (self.stats[PV]+self.stats[PVMAX])/2
			self.world.board['humans'][self.x,self.y] -= 1 
		
