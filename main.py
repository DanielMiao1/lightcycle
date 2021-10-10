"""
LightCycle Game: PyGame version
←↑→↓ for player 1
WASD for player 2
"""
try:
	import pygame
	from pygame.math import Vector2
except ModuleNotFoundError:
	__import__("os").system("pip3 install pygame")
	import pygame
	from pygame.math import Vector2

N = 30  # N is the number of squares on a side of the screen
WIDTH = 20  # WIDTH is the size of a square in pixels

from enum import Enum

class Outcome(Enum):
	none, player1, player2, draw = 0, 1, 2, 3


class Bike:
	def __init__(self, symbol, position, direction):
		"""Bike Class"""
		self.position = position
		self.symbol = symbol
		self.direction = direction
	
	def update_position(self) -> tuple:
		"""Gets the coordinate move"""
		self.position = self.position + self.direction

	def changeDirection(self, direction) -> None:
		"""Changes the direction"""
		self.direction = direction
	
	def in_bounds(self) -> bool:
		"""Returns True if bike is in bounds, False otherwise"""
		return self.position[0] >= 0 and self.position[0] < N and self.position[1] >= 0 and self.position[1] < N

	def __repr__(self):
		return f"{self.symbol} Bike at {self.position}"


class Grid:
	def __init__(self):
		"""Maintain the state of the grid"""
		# boxes are 20px by 20px
		self.squares = [[" " for _ in range(N)] for _ in range(N)]

	def placeMove(self, player: Bike) -> None:
		"""Makes a move for player"""
		#print(player.position[0], player.position[1]
		self.squares[int(player.position[0])][int(player.position[1])] = player.symbol
	
	
	def playerWon(self, player1, player2):
		"""Checks if a player won TODO: If both players exit the board simultaneously (and some other stuff)
		"""
		# 1. neither player has won: 0
		# 2. player 1 won: 1
		# 3. player 2 won: 2
		# 4. both players tie: 3
		# if player1.position == player2.position:
		# 	return Outcome.draw
		# check if in bounds
		if not player1.in_bounds() and not player2.in_bounds():
			return Outcome.draw
		if not player1.in_bounds():
			return Outcome.player2
		if not player2.in_bounds():
			return Outcome.player1

		# one player touches another one
		player1_position = {"x": int(player1.position[0]), "y": int(player1.position[1])}
		player2_position = {"x": int(player2.position[0]), "y": int(player2.position[1])}
		print(self.squares[player1_position["x"]][player1_position["y"]])

		p1_over = self.squares[player1_position["x"]][player1_position["y"]] != ' '
		p2_over = self.squares[player2_position["x"]][player2_position["y"]] != ' '

		if p1_over and p2_over:
			return Outcome.draw

		# If a player runs into another
		if p1_over:
			return Outcome.player2

		elif p2_over:
			return Outcome.player1

		return Outcome.none

	def paint_screen(self, screen):
		"""draw every square in the grid onto the screen based on the symbol"""
		for i, row in enumerate(self.squares):
			for j, _ in enumerate(row):
				if self.squares[i][j] == 'R':
					color = (255, 0, 0)
				elif self.squares[i][j] == 'B':
					color = (0, 0, 255)
				else:
					color = (255, 255, 255)
				pygame.draw.rect(screen, color, (i * WIDTH, j * WIDTH, WIDTH, WIDTH))
		
class Main: # Main class
	def __init__(self):
		pygame.init() # Initialize PyGame
		pygame.display.set_caption("Light Cycle") # Set window title
		# PyGame Variables
		self.screen = pygame.display.set_mode((WIDTH * N, WIDTH * N)) # Set screen
		self.clock = pygame.time.Clock() # Set clock
		# Make instances of classes
		self.player1 = Bike("R", Vector2(0, -1), Vector2(0, 1)) # Set player1 in the top left corner
		self.player2 = Bike("B", Vector2(N - 1, N), Vector2(0, -1)) # Set player2 in the bottom right corner
		self.grid = Grid() # Set grid
		self.running = True

	def run(self): # The main
		"""PyGame Main Loop"""
		UPDATE = pygame.USEREVENT
		pygame.time.set_timer(UPDATE, 200)
		while True:
			for i in pygame.event.get():
				if i.type == pygame.QUIT: exit()
				# Key presses
				if i.type == pygame.KEYDOWN:
					if i.key == pygame.K_LEFT and self.player1.direction != Vector2(1, 0):
						self.player1.changeDirection(Vector2(-1, 0))
					if i.key == pygame.K_RIGHT and self.player1.direction != Vector2(-1, 0):
						self.player1.changeDirection(Vector2(1, 0))
					if i.key == pygame.K_UP and self.player1.direction != Vector2(0, 1):
						self.player1.changeDirection(Vector2(0, -1))
					if i.key == pygame.K_DOWN and self.player1.direction != Vector2(0, -1):
						self.player1.changeDirection(Vector2(0, 1))
					if i.key == pygame.K_a and self.player2.direction != Vector2(1, 0):
						self.player2.changeDirection(Vector2(-1, 0))
					if i.key == pygame.K_s and self.player2.direction != Vector2(0, -1):
						self.player2.changeDirection(Vector2(0, 1))
					if i.key == pygame.K_d and self.player2.direction != Vector2(-1, 0):
						self.player2.changeDirection(Vector2(1, 0))
					if i.key == pygame.K_w and self.player2.direction != Vector2(0, 1):
						self.player2.changeDirection(Vector2(0, -1))
				if i.type == UPDATE and self.running:
					self.update()

			self.screen.fill((255, 255, 255))
			self.grid.paint_screen(self.screen)
			pygame.display.update()
			try: self.clock.tick(60)
			except KeyboardInterrupt: exit()

	def update(self) -> None: # Updater
		"""
		Update Function:
			ask player 1 and player 2 for a move
			place move for player 1, place move for player 2
			check if either player won or if it's a tie
		"""
		# Update the position
		self.player1.update_position()
		self.player2.update_position()

		player_won = self.grid.playerWon(self.player1, self.player2)
		if player_won != Outcome.none:
			
			if player_won == Outcome.draw:
				print("Tie game")
			elif player_won == Outcome.player1:
				print("Player 1 won")
			elif player_won == Outcome.player2:
				print("Player 2 won")

			self.running = False
			return

		# Update the grid
		self.grid.placeMove(self.player1)
		self.grid.placeMove(self.player2)

		# for row in self.grid.squares:
		# 	for square in row:
		# 		print(square, end=",")
		# 	print()
		# self.grid.playerWon(self.player1, self.player2)
		# print(self.grid)
	

# panel with text on it for game over screen


def main():
	m = Main()
	m.run()


if __name__ == "__main__": main()



# 1. bike updates its position
# 2. detects if bike's position is out of bounds
# 3. grid places bike's move into 2d array
# 4. grid paints itself onto screen


# is the game over?
# in bounds
# moving onto an empty square
# tie


"""xx
 x
 x
					0
					0
					0"""

# go backwards by pressing two keys