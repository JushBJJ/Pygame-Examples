"""Collect Coins Game."""
import pygame
from game import *
from titlescreen import *
from level1 import *

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))

done = False

game = Game()

# Titlescreen
room = game.add_room(Titlescreen(game))

# Level 1
room = game.add_room(Level1(game))

# Game
game.switch_room("Titlescreen")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    game.update()
    pygame.display.flip()

pygame.quit()
