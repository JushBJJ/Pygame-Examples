"""Player."""
import pygame
from rectangle import Rectangle


class Player(pygame.sprite.Sprite, Rectangle):
    """Player."""

    def __init__(self, name, pos, width, height, color):
        """Init Player."""
        pygame.sprite.Sprite.__init__(self)
        Rectangle.__init__(self, name, pos, width, height, color)

        self.speed = 5
        self.direction = "right"

        self.controls = {
            "movement": {
                str(pygame.K_w): (0, -self.speed, "up"),
                str(pygame.K_a): (-self.speed, 0, "left"),
                str(pygame.K_s): (0, self.speed, "down"),
                str(pygame.K_d): (self.speed, 0, "right")
            },
            # TODO: Jump function
            "functions": {}
        }

    def controlsEvent(self):
        """Control events."""
        keys = pygame.key.get_pressed()

        # Movement
        for name, value in self.controls["movement"].items():
            if keys[int(name)]:
                self.changePos(self.x+value[0], self.y+value[1])
                self.direction = value[2]
                break

        # TODO: Functions

    def update(self):
        """Update."""
        self.controlsEvent()
