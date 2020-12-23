"""Rectangle."""

import pygame
from rectangle import Rectangle


class Block(pygame.sprite.Sprite, Rectangle):
    """Block."""

    def __init__(self, name, pos, width, height, color):
        """
        Initialize Block.

        Args:
            pos (tuple): Position of the block.
            width ([type]): Width of the block.
            height ([type]): Height of the block.
            color ([type]): Color of the block.
        """
        pygame.sprite.Sprite.__init__(self)
        Rectangle.__init__(self, name,  pos, width, height, color)

        self.solid = True
