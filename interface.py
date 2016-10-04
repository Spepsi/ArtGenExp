import numpy as np
import random
import pygame

resX = 640
resY = 480
debug_lignes = False

# Color
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW =(255, 255, 255)
CYAN   =(  0, 255,   0)
MAJENTA=(255,   0, 255)
DRKGRAY=( 50,  50,  50)

dicColor = {"water":BLUE, 
			"food":GREEN, 
			"rock":DRKGRAY,
			"pheromones":CYAN,
			"humans":RED}

def main(world):
	pygame.init()
	fenetre = pygame.display.set_mode((resX, resY))
	continuer = True
	clock = pygame.time.Clock()
	while continuer:
		draw(fenetre, world)
		world.do()
		clock.tick(10)


def draw(fenetre, world):
	# TODO : get the real world
	board = world.board
	fenetre.fill(BLACK)
	if board is not None:
		nbCaseX = len(board["water"])
		nbCaseY = len(board["water"])
		sizeCaseX = 1.0 * resX / nbCaseX
		sizeCaseY = 1.0 * resY / nbCaseY
		# draw water, rock, food
		for key in ["water","food","rock"]:
			for i in range(len(board[key])):
				for j in range(len(board[key][0])):
					if board[key][i,j]>0:
						pygame.draw.rect(fenetre, 
										dicColor[key], 
										[i*sizeCaseX,j*sizeCaseY,sizeCaseX,sizeCaseY])
		# draw humans and pheromones
		for key in ["pheromones","humans"]:
			for i in range(len(board[key])):
				for j in range(len(board[key][0])):
					if board[key][i,j]>0:
						for k in range(int(board[key][i,j])):
							xrand = i*sizeCaseX + random.random()*sizeCaseX
							yrand = j*sizeCaseY + random.random()*sizeCaseY
							pygame.draw.rect(fenetre,dicColor[key],[xrand,yrand,1,1])
	else:
		nbCaseX = 100
		nbCaseY = 50
		sizeCaseX = 1.0 * resX / nbCaseX
		sizeCaseY = 1.0 * resY / nbCaseY

	# DEBUG : afficher les lignes
	if debug_lignes:
		for i in range(nbCaseX):
			pygame.draw.line(fenetre, WHITE, [i*sizeCaseX,0], [i*sizeCaseX,resY],1)
		for j in range(nbCaseY):
			pygame.draw.line(fenetre, WHITE, [0,j*sizeCaseY], [resX,j*sizeCaseY],1)
	pygame.display.flip()

