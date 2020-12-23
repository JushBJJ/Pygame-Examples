"""Level1."""
import pygame
from player import Player
from block import Block
from room import Room
from coin import Coin


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
            Player("Player", (100, 100), 64, 64, (0, 0, 255)))
        self.createInstance(Block("Block", (100, 300), 64, 64, (255, 130, 70)))
        self.createInstance(Coin("Coin", (100, 550), 64, 64, (255, 255, 0)))

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

    def update(self):
        """Update."""
        self.fonts["Coins"]["text"] = "Coins: "+str(self.player.coins)
        self.updateRoom()
