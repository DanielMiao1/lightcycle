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


class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.resize(400, 400)
		self.setWindowTitle("Light Cycle")
		self.setStyleSheet("background-color: blue;")
		self.update_timer = QTimer(self)
		self.update_timer.setInterval(750)
		self.update_timer.start()

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


try:
	application, window = QApplication([]), Window()
	application.exec_()
except KeyboardInterrupt:
	exit()
