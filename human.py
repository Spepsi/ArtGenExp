import numpy as np
import random



nb_sight = 2
nb_cells_visible = (1+nb_sight*2)**2
nb_stats = 5
nb_ressources = 5
pv_max = 50
proba_mutation = 0.02
shape_dna = (4,nb_cells_visible*nb_ressources+nb_stats)
shape_dna2 = (4,4)
X = 0
Y = 1
EAT = 2
FUCK = 3

PVMAX = 0
STAMINA = 1
SIGHT = 2
PV = 3
AGE = 4


maturity = 2

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
				stats[j] = int(pv_max*np.random.random())
		else:
			stats[j] =  (parent1.stats[j]  if np.random.random()>0.5 else parent2.stats[j])

	stats[PV] = stats[PVMAX]
	stats[AGE] =0
	# Mutation !!!!
	return dna,stats

class Human:
	def __init__(self,world,idx,parent1=None,parent2=None,x=0,y=0):
		self.world = world
		self.dna = np.zeros(shape_dna)
		self.stats = np.zeros(nb_stats-1)
		self.idx = idx
		
		if parent1==None and parent2==None:
			self.dna = np.random.randn(*shape_dna)
			self.stats = np.random.randn(nb_stats)
			self.stats[PVMAX] = int(pv_max*np.random.random())	
			self.stats[SIGHT] = int(4*np.random.random())
			self.x = x
			self.y = y
		else:
			self.dna,self.stats = merge_dna(parent1,parent2)
			self.x = parent1.x
			self.y = parent1.y

		self.stats[PV] = self.stats[PVMAX]


	def do(self):
		# TODO : remove random sensitivy
		self.stats[AGE]+=1
		# Choose the action
		

		# Calculate sightbox
		
		idx = 0


		vec_sight = np.ravel(self.world.board['water'][self.x-nb_sight:self.x+nb_sight+1,self.y-nb_sight:self.y+nb_sight+1])		
		vec_sight = np.concatenate([vec_sight,np.ravel(self.world.board['humans'][self.x-nb_sight:self.x+nb_sight+1,self.y-nb_sight:self.y+nb_sight+1])])
		vec_sight = np.concatenate([vec_sight,np.ravel(self.world.board['rock'][self.x-nb_sight:self.x+nb_sight+1,self.y-nb_sight:self.y+nb_sight+1])])
		vec_sight = np.concatenate([vec_sight,np.ravel(self.world.board['food'][self.x-nb_sight:self.x+nb_sight+1,self.y-nb_sight:self.y+nb_sight+1])])
		vec_sight = np.concatenate([vec_sight,np.ravel(self.world.board['pheromones'][self.x-nb_sight:self.x+nb_sight+1,self.y-nb_sight:self.y+nb_sight+1])])
		# vec_sight = np.concatenate([vec_sight,np.ravel(self.world.board['food'][self.x-nb_sight:self.x+nb_sight+1,self.y-nb_sight:self.y+nb_sight+1])])
		
		# Calculate stats
		stats = self.stats
		inputs = np.concatenate([vec_sight,stats])
		output = np.tanh(np.dot(self.dna,inputs))
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
		if action==X or action==Y or (action==FUCK and self.stats[AGE]<maturity) or (action==EAT and self.world.board['food'][self.x,self.y] < 1) :
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
		# print 'moved from '+str(x_or)+','+str(y_or)+' to '+str(self.x)+','+str(self.y)
		assert np.abs(x_or-self.x)+np.abs(y_or-self.y)<=1, "erreur norme"
		

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
			self.world.create_human(Human(self.world,self.world.idx,parent1=self,parent2=partner))
			self.world.idx += 1
			self.stats[AGE] =0
			

	def eat(self):
		# Remove food from board
		if self.world.board['food'][self.x,self.y] > 0:
			self.stats[PV] = (self.stats[PV]+self.stats[PVMAX])/2
			self.world.board['food'][self.x,self.y] -= 1 
		
