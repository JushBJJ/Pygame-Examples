"""Coin."""

import pygame
from rectangle import Rectangle
import random


class Coin(pygame.sprite.Sprite, Rectangle):
    """Coin."""

    def __init__(self, name, pos, width, height, color):
        """
        Initialize Coin.

        Args:
            pos (tuple): Position of the coin.
            width ([type]): Width of the coin.
            height ([type]): Height of the coin.
            color ([type]): Color of the coin.
        """
        pygame.sprite.Sprite.__init__(self)
        Rectangle.__init__(self, name, pos, width, height, color)

        self.coin = True
        self.instanceGroup = None

    def update(self):
        """Update."""
        sprites = pygame.sprite.spritecollide(self, self.instanceGroup, False)

        for sprite in sprites:
            if hasattr(sprite, "player"):
                sprite.coins += 1

                self.changePos(random.randrange(300, 600),
                               random.randrange(200, 400))
                return 1
