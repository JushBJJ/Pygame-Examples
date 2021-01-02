"""Collect Coins Game."""
import pygame

from game import Game
from titlescreen import Titlescreen
from level1 import Level1

pygame.init()
screen = pygame.display.set_mode((800, 600))

done = False
clock = pygame.time.Clock()
game = Game()

# Rooms
game.add_room(Titlescreen(game))
game.add_room(Level1(game))

# Game
game.switch_room("Titlescreen")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    game.update()
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
