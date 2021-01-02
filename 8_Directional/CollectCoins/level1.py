"""Level1."""
import pygame
from player import Player
from block import Block
from room import Room
from coin import Coin

import numpy as np
from PIL import Image


class Level1(pygame.sprite.Sprite, Room):
    """Level 1."""

    def __init__(self, game):
        """
        Initialize the room.

        Args:
            game (class<game>): Game class
        """
        pygame.sprite.Sprite.__init__(self)
        Room.__init__(self, "Level1")
        self.game = game
        self.player = None

        # Instances
        self.player = self.createInstance(
            Player("Player", (400, 400), 64, 64, (0, 0, 255), room=self))
        self.createInstance(Block("Block", (400, 300), 64, 64, (255, 130, 70)))
        self.createInstance(Coin("Coin", (300, 450), 64, 64, (255, 255, 0)))

        # Creating Barrier
        # * For Top
        x = -32
        while x < 800:
            self.createInstance(
                Block("Block", (x+64, 0), 64, 64, (255, 130, 70)))
            x += 64

        # * For Bottom
        x = -32
        while x < 800:
            self.createInstance(
                Block("Block", (x+64, 600), 64, 64, (255, 130, 70)))
            x += 64

        # * For Left Side
        y = 0
        while y < 600:
            self.createInstance(
                Block("Block", (0, y+64), 64, 64, (255, 130, 70)))

            y += 64

        # * For Right Side
        y = 0
        while y < 600:
            self.createInstance(
                Block("Block", (800, y+64), 64, 64, (255, 130, 70)))

            y += 64

        # Create text
        self.createFont("Title", "dejavusansmono", 20,
                        (750, 16), "Level1", (255, 255, 255))

        self.createFont("Coins", "dejavusansmono", 20, (70, 16),
                        "Coins: Not loaded.", (255, 255, 255))

    def go_to_level(self):
        """Go to the next level."""
        timer = self.getTimer("M Press2")

        if timer["done"] == True:
            self.game.switch_room("Titlescreen")
            self.resetTimer("M Press2")

    def getEnviornment(self):
        """rect = self.screen.get_rect()
        width = rect.width
        height = rect.height

        env = pygame.image.tostring(self.screen, "RGB")
        image = Image.frombytes("RGB", (width, height), env)

        image = image.resize((1, 1024))
        image = image.convert("L")
        matrix = np.asarray(image.getdata())

        matrix = (matrix - 128)/(128 - 1)
###"""
        coin = self.getInstance("Coin")
        player = self.getInstance("Player")

        playerX = player.pX
        playerY = player.pX

        coinX = coin.x
        coinY = coin.y

        ret = np.asarray([playerX, playerY, coinX, coinY])

        return ret

    def update(self):
        """Update."""
        self.fonts["Coins"]["text"] = "Coins: "+str(self.player.coins)
        self.updateRoom()
