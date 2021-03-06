import numpy as np
from human import Human
import random


nb_foyer_humans = 4
nb_humans_start = 500


nb_sight = 2

proba_food = 0.05
proba_water = 0.005
proba_rock = 0.2
max_pop = 20
max_total_pop = 1500
kill = 2*max_pop/3
debug = True

PVMAX = 0
STAMINA = 1
SIGHT = 2
PV = 3
AGE = 4

class World:
	def __init__(self,sizeX,sizeY):
		self.to_be_born = []
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
		self.cases = [[[] for j in range(self.sizeY)] for i in range(self.sizeX)]

		# Generate random initialization
		# Humans
		self.humans = {}
		for _ in range(nb_foyer_humans):
			x_foyer = int(max(10,min(sizeX-10,(2.0*np.random.random())*sizeX/2)))
			y_foyer = int(max(10,min(sizeY-10,(2.0*np.random.random())*sizeY/2)))
			for _ in range(nb_humans_start):
				self.create_human(Human(self,self.idx,x=x_foyer,y=y_foyer))
				self.idx+=1

		# rock et water de base
		for i in range(1,sizeX-1):
			for j in range(1,sizeY-1):
				d = 1.0-4.0*(min(i,sizeX-i)*min(i,sizeX-i)+min(j,sizeY-j)*min(j,sizeY-j))/(sizeX*sizeY)
				if np.random.random()<d*proba_rock:
					self.board['rock'][i,j] = 1
				if np.random.random()<(1.0-d)*proba_water:
					self.board['water'][i,j] = 1
		# propagate rock into mountains
		proba_rock_propagate = 0.13
		to_add_rock = []
		for i in range(1,sizeX-1):
			for j in range(1,sizeY-1):
				if self.is_food_possible(i,j):
					p = 0
					for delta in [[1,0],[-1,0],[0,1],[0,-1]]:
						i2,j2 = i,j
						i2 += delta[0]
						j2 += delta[1]
						if i2>=0 and j2>=0 and i2<sizeX and j2<sizeY and self.board["rock"][i2,j2]>0:
							p += proba_rock_propagate
						if np.random.random()<p:
							to_add_rock.append([i,j])
		for a in to_add_rock:
			self.board["rock"][a[0],a[1]] = 1
		# propagate water into river
		proba_water_propagate = 0.13
		for n in range(20):
			for i in range(1,sizeX-1):
				for j in range(1,sizeY-1):
					if self.is_water_possible(i,j):
						p = 0
						for delta in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[-1,1],[1,-1]]:
							i2,j2 = i,j
							for edge in range(5):
								i2 += delta[0]
								j2 += delta[1]
								if i2>=0 and j2>=0 and i2<sizeX and j2<sizeY and self.board["water"][i2,j2]>0:
									p += proba_water_propagate
								else:
									break
							if edge>0:
								p-= proba_water_propagate/0.9
						if np.random.random()<p:
							self.board["water"][i,j] += 1
		# feed the rivers
		for n in range(2):
			for i in range(1,sizeX-1):
				for j in range(1,sizeY-1):
					if self.is_water_possible(i,j):
						p = 0
						for delta in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[-1,1],[1,-1]]:
							i2,j2 = i,j
							i2 += delta[0]
							j2 += delta[1]
							if i2>=0 and j2>=0 and i2<sizeX and j2<sizeY and self.board["water"][i2,j2]>0:
								p += proba_water_propagate/3.0
							if np.random.random()<p:
								self.board["water"][i,j] += 1
		# initialise food
		for n in range(30):
			self.do_food()
		# draw map borders
		for i in range(sizeX):
			for j in range(6):
				self.board['water'][i,j] = 1
				self.board['water'][i,sizeY-j-1] = 1
				self.board['food'][i,j] = 0
				self.board['food'][i,sizeY-j-1] = 0
				self.board['rock'][i,j] = 0
				self.board['rock'][i,sizeY-j-1] = 0
		for i in range(6):
			for j in range(sizeY):
				self.board['water'][i,j] = 1
				self.board['water'][sizeX-i-1,j] = 1
				self.board['food'][i,j] = 0
				self.board['food'][sizeX-i-1,j] = 0
				self.board['rock'][i,j] = 0
				self.board['rock'][sizeX-i-1,j] = 0

		# food
		# rock

	def create_human(self,human):
		self.to_be_born.append(human)


	def get_humans_in_case(self,x,y):
		tab= []
		for i in self.cases[x][y]:
			tab.append(self.humans[i])
		return tab

	def do(self):
		print 'pop' + str(np.sum(self.board['humans']))
		self.do_food()

		# Handle born
		for h in self.to_be_born:
			self.humans[h.idx] = h
			self.board['humans'][h.x,h.y]+=1
			self.cases[int(h.x)][int(h.y)].append(h.idx)
		self.to_be_born = []

		to_remove = []
		if np.max(self.board['humans'])>max_pop:
			
			# Look for cells in max pop ...
			for i in range(self.sizeX):
				for j in range(self.sizeY):
					if self.board['humans'][i,j]>max_pop:
						humans = self.get_humans_in_case(i,j)
						
						random.shuffle(humans)
						humans = humans[0:kill]
						
						to_remove = humans


		pop = np.sum(self.board['humans'])

		if pop>max_total_pop:
			
			nb_to_kill = int(pop - max_total_pop)
			humans = list(self.humans.values())
			
			random.shuffle(humans)
			humans = humans[0:nb_to_kill]
			
			[to_remove.append(h) for h in humans]

		# handling death
		for idx,i in enumerate(self.humans):
			h = self.humans[i]
			h.stats[PV]-=1
			if h.stats[PV]<=0 or self.board['water'][h.x,h.y]>0 or self.board['rock'][h.x,h.y]>0:
				to_remove.append(h)

		for h in to_remove:
			if h.idx in self.humans:
				del self.humans[h.idx]
				self.board['humans'][h.x,h.y]-=1
				self.cases[h.x][h.y].remove(h.idx)

		# preprocessing human actions
		self.preprocessSight = [[None for j in range(self.sizeY)] for i in range(self.sizeX)]

		for i in range(self.sizeX):
		 	for j in range(self.sizeY):
		 		if len(self.cases[i][j])>0:
		 			vec_sight = []
		 			for key in ["food","humans","rock","water","pheromones"]:
		 				l = np.sum(self.board[key][i-nb_sight:i+1,j-nb_sight:j+nb_sight+1])
		 				r = np.sum(self.board[key][i:i+nb_sight+1,j-nb_sight:j+nb_sight+1])
		 				u = np.sum(self.board[key][i-nb_sight:i+nb_sight+1,j-nb_sight:j+1])
		 				d = np.sum(self.board[key][i-nb_sight:i+nb_sight+1,j:j+nb_sight+1])
		 				c = self.board[key][i,j]
		 				vec_sight+=[l,r,d,u,c]
		 			self.preprocessSight[i][j] = vec_sight


		# for i in range(self.sizeX):
		# 	for j in range(self.sizeY):
		# 		if len(self.cases[i][j])>0:
		# 			vec_sight = np.ravel(self.board['water'][i-nb_sight:i+nb_sight+1,j-nb_sight:j+nb_sight+1])		
		# 			vec_sight = np.concatenate([vec_sight,np.ravel(self.board['humans'][i-nb_sight:i+nb_sight+1,j-nb_sight:j+nb_sight+1])])
		# 			vec_sight = np.concatenate([vec_sight,np.ravel(self.board['rock'][i-nb_sight:i+nb_sight+1,j-nb_sight:j+nb_sight+1])])
		# 			vec_sight = np.concatenate([vec_sight,np.ravel(self.board['food'][i-nb_sight:i+nb_sight+1,j-nb_sight:j+nb_sight+1])])
		# 			vec_sight = np.concatenate([vec_sight,np.ravel(self.board['pheromones'][i-nb_sight:i+nb_sight+1,j-nb_sight:j+nb_sight+1])])
		# 			self.preprocessSight[i][j] = vec_sight

		# handling human actions
		for h in self.humans.values():
			h.do()

		for i in range(self.sizeX):
			for j in range(self.sizeY):
				self.board['pheromones'][i,j] = max(0,self.board['pheromones'][i,j]-1)

	def is_food_possible(self,i,j):
		return self.board["rock"][i,j]==0 and self.board["water"][i,j]==0
	def is_water_possible(self,i,j):
		return self.board["rock"][i,j]==0
	def do_food(self):
		# Create food
		proba_new_food = 0.5
		while np.random.random()<proba_new_food:
			i = np.random.randint(1,self.sizeX-1)
			j = np.random.randint(1,self.sizeY-1)
			if self.is_food_possible(i,j):
				self.board["food"][i,j]+=1
		# Propagate food
		proba_food_propagate = 0.05
		proba_food_growth = 0.05
		for i in range(1,self.sizeX-1):
			for j in range(1,self.sizeY-1):
				if self.board["food"][i,j]>0:
					p = proba_food_growth/4
					for i2,j2 in [[i-1,j],[i+1,j],[i,j-1],[i,j+1]]:
						if self.board["water"][i2,j2]>0:
							p += proba_food_growth
						p+= proba_food_growth * (self.board["food"][i2,j2]-1) / 4
					if np.random.random()<p:
						self.board["food"][i,j]+=1
				elif self.is_food_possible(i,j):
					p = 0
					for i2,j2 in [[i-1,j],[i+1,j],[i,j-1],[i,j+1]]:
						p += proba_food_propagate*self.board["food"][i2,j2]
					if np.random.random()<p:
						self.board["food"][i,j] += 1



