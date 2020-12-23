"""Player."""
import pygame
from rectangle import Rectangle


class Player(pygame.sprite.Sprite, Rectangle):
    """Player."""

    def __init__(self, name, pos, width, height, color, **kwargs):
        """
        Initialize Player.

        Args:
            pos (tuple): Position of the Player.
            width ([type]): Width of the Player.
            height ([type]): Height of the Player.
            color ([type]): Color of the Player.
        """
        pygame.sprite.Sprite.__init__(self)
        Rectangle.__init__(self, name, pos, width, height, color)

        self.speed = 5
        self.direction = "right"
        self.player = True
        self.coins = 0

        # * Will be automatically set at the createInstance() function.
        self.instanceGroup = None

        self.controls = {
            "movement": {
                str(pygame.K_w): (0, -self.speed, "up"),
                str(pygame.K_a): (-self.speed, 0, "left"),
                str(pygame.K_s): (0, self.speed, "down"),
                str(pygame.K_d): (self.speed, 0, "right"),
                str(pygame.K_w+pygame.K_a): "upleft",
                str(pygame.K_w+pygame.K_d): "upright",
                str(pygame.K_s+pygame.K_a): "downleft",
                str(pygame.K_s+pygame.K_d): "downright",
            },
            # TODO: Jump function
            "functions": {}
        }

        self.collisionEvents = {
            "right": (-self.speed, 0),
            "left": (self.speed, 0),
            "up": (0, self.speed),
            "down": (0, -self.speed),

            # * All speed in this section is multiplied by 0.0707 because
            # * when it moves diagonally, it moves 1.414 times faster
            # * Reference: https://digisoln.com/gamemaker/gml/topdownplayer

            "upright": (-self.speed*0.707, self.speed*0.707),
            "upleft": (self.speed*0.707, self.speed*0.707),
            "downright": (-self.speed*0.707, -self.speed*0.707),
            "downleft": (self.speed*0.707, -self.speed*0.707)
        }

    def controlsEvent(self):
        """Control events."""
        keys = pygame.key.get_pressed()

        # Movement
        for name, value in self.controls["movement"].items():
            if keys[int(name)]:
                self.changePos(self.x+value[0], self.y+value[1])
                self.direction = value[2]

                # Upright, Upleft, Downright, Downleft
                for name2, value2 in self.controls["movement"].items():
                    if keys[int(name2)] and name != name2:
                        num = str(int(name)+int(name2))

                        # * Fixes crash where A and D or W and S are pressed.
                        if num not in self.controls["movement"].keys():
                            continue

                        self.changePos(self.x+value2[0], self.y+value2[1])
                        self.direction = self.controls["movement"][num]
                break  # * Used to stop unnecessary speeding.

        # TODO: Functions

    def collideEvent(self, touching):
        """
        Collision event for the player.

        Args:
            touching (sprite): Sprite that has been collided with the player.
        """
        while self.rect.colliderect(touching.rect):
            newX = self.x+self.collisionEvents[self.direction][0]
            newY = self.y+self.collisionEvents[self.direction][1]

            self.changePos(newX, newY)

    def touchEvent(self):
        """Touch event."""
        touching = pygame.sprite.spritecollide(self, self.instanceGroup, False)

        for sprite in touching:
            if hasattr(sprite, "solid"):
                if getattr(sprite, "solid") == True:
                    self.collideEvent(sprite)

    def update(self):
        """Update."""
        self.controlsEvent()
        self.touchEvent()

        print("Coins: "+str(self.coins))
