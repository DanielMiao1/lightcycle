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


class Button:
	"""Button widget"""
	def __init__(self, screen, text: str = "", pos: Vector2 = Vector2(0, 0), size: tuple = (20, 20), color: tuple or set or list = (255, 0, 0), button_color: tuple or set or list = (0, 255, 255)):
		self.screen = screen
		self.button = pygame.Surface(size)
		self.button.fill(button_color)
		self.rect = self.button.get_rect(center=tuple(pos))
		self.button_text = text
		self.font_size = 32
		self.text_color = color
		self.background_color = button_color
		button_font = pygame.font.SysFont(None, self.font_size)
		self.text = button_font.render(self.button_text, False, color)

	def setBackgroundColor(self, color):
		self.background_color = color
		self.button.fill(color)
	
	def setTextColor(self, color):
		self.text_color = color
		self.text = pygame.font.SysFont(None, self.font_size).render(self.button_text, False, color)

	def setText(self, text):
		self.button_text = text
		self.text = pygame.font.SysFont(None, self.font_size).render(text, False, self.text_color)

	def clicked(self, pos):
		return self.rect.collidepoint(*pos)

	def paint_widget(self):
		"""Paint the button to the screen"""
		self.button.blit(self.text, ((self.rect.width - self.text.get_rect().width) // 2, (self.rect.height - self.text.get_rect().height) // 2))
		self.screen.blit(self.button, self.rect)


# class EndScreen:
# 	"""Ending Screen"""
# 	def __init__(self, screen, outcome):
# 		self.screen = screen
# 		self.outcome = outcome
	
# 	def paint_widget(self):
# 		# self.screen.blit()


class Bike:
	def __init__(self, symbol, position, direction):
		"""Bike Class"""
		self.position = position
		self.symbol = symbol
		self.direction = direction
		self.direction_changed = False
	
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

		p1_over = self.squares[player1_position["x"]][player1_position["y"]] != ' '
		p2_over = self.squares[player2_position["x"]][player2_position["y"]] != ' '

		# check if the head of player1 and player2 are at the same position
		if (p1_over and p2_over) or player1_position == player2_position:
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

# title text
# button (surface to click)

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
		self.started = False
		self.start_button = Button(self.screen, text="Start Game", pos=Vector2(WIDTH * N / 2, WIDTH * N / 2), size=(225, 75), color=(255, 255, 255), button_color=(0, 0, 0))
		self.ending = Outcome.none
		self.ending_text = pygame.font.SysFont(None, 40).render("Tie Game" if self.ending == Outcome.draw else "Player 1 wins" if self.ending == Outcome.player1 else "Player 2 wins", False, (0, 0, 0))
		self.ending_text_rect = self.ending_text.get_rect(center=(WIDTH * N / 2, WIDTH * N / 2))

	def run(self): # The main
		"""PyGame Main Loop"""
		UPDATE = pygame.USEREVENT
		pygame.time.set_timer(UPDATE, 200)
		while True:
			if not self.started:
				for i in pygame.event.get():
					if i.type == pygame.MOUSEBUTTONDOWN:
						if self.start_button.clicked(i.pos):
							self.started = True
			else:
				for i in pygame.event.get():
					if i.type == pygame.QUIT: exit()
					# Key presses
					if i.type == pygame.KEYDOWN:
						if not self.player1.direction_changed:
							if i.key == pygame.K_LEFT and self.player1.direction != Vector2(1, 0):
								self.player1.changeDirection(Vector2(-1, 0))
								self.player1.direction_changed = True
							elif i.key == pygame.K_RIGHT and self.player1.direction != Vector2(-1, 0):
								self.player1.changeDirection(Vector2(1, 0))
								self.player1.direction_changed = True
							elif i.key == pygame.K_UP and self.player1.direction != Vector2(0, 1):
								self.player1.changeDirection(Vector2(0, -1))
								self.player1.direction_changed = True
							elif i.key == pygame.K_DOWN and self.player1.direction != Vector2(0, -1):
								self.player1.changeDirection(Vector2(0, 1))
								self.player1.direction_changed = True
						if not self.player2.direction_changed:
							if i.key == pygame.K_a and self.player2.direction != Vector2(1, 0):
								self.player2.changeDirection(Vector2(-1, 0))
								self.player2.direction_changed = True
							elif i.key == pygame.K_s and self.player2.direction != Vector2(0, -1):
								self.player2.changeDirection(Vector2(0, 1))
								self.player2.direction_changed = True
							elif i.key == pygame.K_d and self.player2.direction != Vector2(-1, 0):
								self.player2.changeDirection(Vector2(1, 0))
								self.player2.direction_changed = True
							elif i.key == pygame.K_w and self.player2.direction != Vector2(0, 1):
								self.player2.changeDirection(Vector2(0, -1))
								self.player2.direction_changed = True
					if i.type == UPDATE and self.running:
						self.update()

			self.screen.fill((255, 255, 255))
			if self.started:
				self.grid.paint_screen(self.screen)
			else:
				self.start_button.paint_widget()
			if self.ending != Outcome.none:
				self.screen.blit(self.ending_text, self.ending_text_rect)
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
		
		self.player1.direction_changed = False
		self.player2.direction_changed = False

		player_won = self.grid.playerWon(self.player1, self.player2)
		if player_won != Outcome.none:
			
			if player_won == Outcome.draw:
				print("Tie game")
			elif player_won == Outcome.player1:
				print("Player 1 won")
			elif player_won == Outcome.player2:
				print("Player 2 won")

			self.running = False
			self.ending = player_won
			self.ending_text = pygame.font.SysFont(None, 40).render("Tie Game" if self.ending == Outcome.draw else "Player 1 wins" if self.ending == Outcome.player1 else "Player 2 wins", False, (0, 0, 0))
			self.ending_text_rect = self.ending_text.get_rect(center=(WIDTH * N / 2, WIDTH * N / 2))
			return
		

		# Update the grid
		self.grid.placeMove(self.player1)
		self.grid.placeMove(self.player2)


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


"""
xx
 x
 x
					0
					0
					0
"""

# go backwards by pressing two keys
