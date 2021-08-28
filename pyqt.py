try: import PyQt5
except ModuleNotFoundError: __import__("os").system("pip3 install PyQt5")

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

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
		"""Get a move"""
		return (0, 0)
	
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
		"""Makes a move for `player`"""
		print(player, position)
	
	def playerWon(self) -> bool:
		"""Checks if a player won"""
		return False

def main():
	m = Main()
	m.run()


if __name__ == "__main__": main()

class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.resize(400, 400)
		self.setWindowTitle("Light Cycle")
		self.setStyleSheet("background-color: white")
		self.rectangle = QWidget(self)
		self.rectangle.resize(50, 80)
		self.rectangle.setStyleSheet("background-color: green")
		
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


application, window = QApplication([]), Window()
application.exec_()
