"""Player."""
import random
import numpy as np
import pygame
from rectangle import Rectangle

# * AI
from model.Model import DQN
import torch.optim as optim
from model.core import ReplayBuffer, print_hyperparamters


class Player(pygame.sprite.Sprite, Rectangle):
    """Player."""

    def __init__(self, name, pos, width, height, color, room):
        """
        Initialize Player.

        Args:
            pos(tuple): Position of the Player.
            width([type]): Width of the Player.
            height([type]): Height of the Player.
            color([type]): Color of the Player.
        """
        pygame.sprite.Sprite.__init__(self)
        Rectangle.__init__(self, name, pos, width, height, color)

        self.speed = 5
        self.direction = "right"
        self.player = True
        self.coins = 0
        self.pX = self.x
        self.pY = self.y

        # AI
        self.model = None
        self.AIKeys = 0
        self.room = room

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

        # AI
        self.AIPress = {
            0: pygame.K_w,
            1: pygame.K_a,
            2: pygame.K_s,
            3: pygame.K_d,
            4: pygame.K_w+pygame.K_a,
            5: pygame.K_w+pygame.K_d,
            6: pygame.K_s+pygame.K_a,
            7: pygame.K_s+pygame.K_d
        }
        self.createAI()
        self.clearKeys = list(pygame.key.get_pressed())

        self.totalrewards = 0

        self.oldX = self.x
        self.oldY = self.y
        self.states = 0
        self.epochsEnd = 1
        self.epochs = 0
        self.initialX = self.x
        self.initialY = self.y

    def createAI(self):
        self.model = DQN(4)

    def runAI(self):
        state = self.room.getEnviornment()
        action = self.model.choose_action(self.room.getEnviornment())
        return state, action

    def controlsEvent(self, AIPress=None):
        """Control events."""
        if AIPress == None:
            keys = pygame.key.get_pressed()
        else:
            self.clearKeys[pygame.K_w] = 0
            self.clearKeys[pygame.K_a] = 0
            self.clearKeys[pygame.K_s] = 0
            self.clearKeys[pygame.K_d] = 0

            keys = self.clearKeys
            keys[self.AIPress[AIPress]] = 1
        # Movement
        for name, value in self.controls["movement"].items():
            if keys[int(name)]:
                self.changePos(self.x+value[0], self.y+value[1])
                self.direction = value[2]

                # Upright, Upleft, Downright, Downleft
                """for name2, value2 in self.controls["movement"].items():
                    if keys[int(name2)] and name != name2:
                        num = str(int(name)+int(name2))

                        # * Fixes crash where A and D or W and S are pressed.
                        if num not in self.controls["movement"].keys():
                            continue

                        self.changePos(self.x+value2[0], self.y+value2[1])
                        self.direction = self.controls["movement"][num]"""
                break  # * Used to stop unnecessary speeding.

        # TODO: Functions

    def collideEvent(self, touching):
        """
        Collision event for the player.

        Args:
            touching(sprite): Sprite that has been collided with the player.
        """
        while self.rect.colliderect(touching.rect):
            newX = self.x+self.collisionEvents[self.direction][0]
            newY = self.y+self.collisionEvents[self.direction][1]

            self.changePos(newX, newY)

    def touchEvent(self):
        """Touch event."""
        touching = pygame.sprite.spritecollide(self, self.instanceGroup, False)
        ret = 0

        for sprite in touching:
            if hasattr(sprite, "solid"):
                if getattr(sprite, "solid") == True:
                    self.collideEvent(sprite)
                    ret -= 1

            elif hasattr(sprite, "coin"):
                ret += 1

        return ret

    def update(self):
        """Update."""
        if self.epochs >= self.epochsEnd:
            self.x = self.initialX
            self.y = self.initialY
            self.epochsEnd += 10
            self.epochs = 0

            self.model.increaseEpilison()
            self.totalrewards = 0

        self.epochs += 1

        state = self.room.getEnviornment()
        self.states += self.model.addState(state)

        probs = self.model.policy(state)
        self.model.lastAction = np.random.choice(
            np.arange(len(probs)), p=probs)

        self.controlsEvent(self.model.lastAction)
        reward = self.touchEvent()
        state_ = self.room.getEnviornment()
        self.states += self.model.addState(state_)
        self.model.step(state, state_, self.model.lastAction, reward)

        self.totalrewards += reward

        self.pX = self.x
        self.pY = self.y
