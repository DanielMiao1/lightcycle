import pygame
pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("Light Cycle")
clock = pygame.time.Clock()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: pygame.quit()

	screen.fill((255, 255, 255))
	pygame.draw.rect(screen, (0, 255, 0), (0, 0, 50, 80))
	pygame.display.update()
	clock.tick(60)