"""Simple Pygame Template."""
import pygame

# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600), vsync=True)
clock = pygame.time.Clock()

# Game Loop
Running = True

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# Quit
pygame.quit()
