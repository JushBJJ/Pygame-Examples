"""Rectangle."""
import pygame


class Rectangle:
    """Rectangle."""

    def __init__(self, name, pos, width, height, color):
        """
        Initialize Rectangle Sprite.

        Args:
            name (string): The name of the sprite
            pos (tuple): Position of the sprite
            width (int): Width of the sprite
            height (int): Height of the sprite
            color (tuple): Color of the sprite
        """
        self.name = name

        self.x = pos[0]
        self.y = pos[1]

        self.width = width
        self.height = height
        self.color = color
        self.show = True

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(center=(pos))

        self.image.fill(self.color)

    def changePos(self, x, y):
        """
        Change the position of the sprite.

        Args:
            x (int): x of the sprite.
            y (int): y of the sprite.
        """
        self.rect.x = self.x = x
        self.rect.y = self.y = y
