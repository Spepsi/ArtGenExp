import numpy as np
import random


nb_cells_visible = 80
nb_stats = 5
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
AGE = 4
maturity = 20

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
				stats[j] = int(4*np.random.random())
			if j==PVMAX:
				stats[j] = int(1*np.random.random())

		else:
			stats[j] =  (parent1.stats[j]  if np.random.random()>0.5 else parent2.stats[j])

	stats[PV] = stats[PVMAX]
	stats[AGE] =0
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
			
			self.stats[PVMAX] = int(30*np.random.random())
			
			self.stats[SIGHT] = int(4*np.random.random())

			self.x = self.world.sizeX/2
			self.y = self.world.sizeY/2

		else:
			self.dna,self.stats = merge_dna(parent1,parent2)
			self.x = parent1.x
			self.y = parent1.y

		self.stats[PV] = self.stats[PVMAX]


	def do(self):
		# TODO : remove random sensitivy
		self.stats[AGE]+=1
		# Choose the action
		output = np.dot(self.dna,np.random.random(self.dna.shape[1]))
		action = np.argmax(np.abs(output))

		if debug:
			print 'action for : '+str(self.idx)
			print 'PV : '+str(self.stats[PV])
			if action==X:
				print 'move X'
			if action == Y:
				print 'move Y'
			if action == EAT:
				print 'eat'
			if action == FUCK:
				print 'fuck'
		if action==X or action==Y:
			self.move(output)
		elif action==EAT:
			self.eat()
		elif action==FUCK:
			self.fuck()


	def move(self,output):

		somme = np.sum(self.world.board['humans'])
		x_or = self.x
		y_or = self.y
		self.world.board['humans'][self.x,self.y]-=1
		newx = self.x
		newy = self.y
		if np.abs(output[0])>np.abs(output[1]):
			newx = int(self.x + (np.sign(output[0])))
		else:
			newy = int(self.y + (np.sign(output[1])))
		if self.world.board['rock'][newx,newy]==0:
			self.x, self.y = newx, newy

		self.world.board['humans'][self.x,self.y]+=1
		somme_end = np.sum(self.world.board['humans'])
		assert somme==somme_end,'error somme : '+str(somme)+' '+str(somme_end)
		assert np.abs(x_or-self.x)+np.abs(y_or-self.y)<=1, "erreur norme"
		# print 'moved from '+str(x_or)+','+str(y_or)+' to '+str(self.x)+','+str(self.y)

	def fuck(self):
		# Get all the humans in the cell
		if self.world.board['humans'][self.x,self.y] > 1 and self.stats[AGE]>maturity:
			# Find another human being
			humans = []
			for h in self.world.humans:
				if h.x==self.x and h.y == self.y and self.idx!=h.idx:
					humans.append(h)
			assert len(humans)==self.world.board['humans'][int(self.x),int(self.y)] -1 , 'Bad update ...'+str(len(humans))+' '+str(self.world.board['humans'][self.x,self.y] -1)
			
			# Choose human at random
			partner = random.choice(humans)
			self.world.create_human(Human(self.world,self.world.idx,self,partner))
			self.world.idx += 1
			

	def eat(self):
		# Remove food from board
		if self.world.board['food'][self.x,self.y] > 0:
			self.stats[PV] = (self.stats[PV]+self.stats[PVMAX])/2
			self.world.board['food'][self.x,self.y] -= 1 
		
