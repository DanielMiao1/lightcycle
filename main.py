try:
	import pygame
	from pygame.math import Vector2
except ModuleNotFoundError:
	__import__("os").system("pip3 install pygame")
	import pygame
	from pygame.math import Vector2

import random

class Direction:
	UP, DOWN, RIGHT, LEFT = 0, 1, 2, 3

class Bike:
	def __init__(self, symbol, start):
		"""Bike Class"""
		self.direction = Direction.UP
		self.position = start
		self.symbol = symbol
	
	def getMove(self) -> tuple:
		"""Gets a move"""
		# if self.position == Direction.UP:
		# 	return ()
	
	def changeDirection(self, direction) -> None:
		"""Changes the direction"""
		self.direction = direction

class Grid:
	def __init__(self):
		"""Maintain the state of the grid"""
		N = 30
		# 20px by 20px
		self.squares = [[0 for _ in range(N)] for _ in range(N)]

	def placeMove(self, player: Bike, position: tuple) -> None:
		"""Makes a move for player"""
		print(player, position)
	
	def playerWon(self) -> bool:
		"""Checks if a player won"""
		return False
		
class Main:
	def __init__(self):
		pygame.init() # Initialize PyGame
		pygame.display.set_caption("Light Cycle") # Set window title
		# PyGame Variables
		self.screen = pygame.display.set_mode((600, 600)) # Set screen
		self.clock = pygame.time.Clock() # Set clock
		# Make instances of classes
		positions = self.generate_start_pos() # Make local instance of positions
		self.player1, self.player2 = Bike("R", positions[0]), Bike("B", positions[1]) # Set bikes
		self.grid = Grid() # Set grid

	def generate_start_pos():
		return random.choice([[Vector2(15, 1), Vector2(15, 29)], [Vector2(15, 29), Vector2(15, 1)], [Vector2(1, 15), Vector2(29, 15)], [Vector2(29, 15), Vector2(1, 15)]])
		
	def run(self):
		"""PyGame Main Loop"""
		UPDATE = pygame.USEREVENT
		pygame.time.set_timer(UPDATE, 750)
		while True:
			for i in pygame.event.get():
				if i.type == pygame.QUIT: exit()
				if i.type == UPDATE: self.update()

			self.screen.fill((255, 255, 255))

			pygame.draw.rect(self.screen, (0, 255, 0), (0, 0, 50, 80))
			# CODE HERE
			
			pygame.display.update()
			try: self.clock.tick(60)
			except KeyboardInterrupt: exit()

	def update(self) -> None:
		"""
		Update Function:
			ask player 1 and player 2 for a move
			place move for player 1, place move for player 2
			check if either player won or if it's a tie
		"""
		self.grid.placeMove(self.player1, self.player1.getMove())
		self.grid.placeMove(self.player2, self.player2.getMove())
		return

def main():
	m = Main()
	m.run()


if __name__ == "__main__": main()