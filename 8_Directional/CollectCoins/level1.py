"""Level1."""
import pygame
from player import Player
from block import Block
from room import Room


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

        # Create text
        self.createFont("Title", "dejavusansmono", 50,
                        (400, 300), "Level1", (255, 255, 255))

        # Height
        height = self.fonts["Title"]["object"].get_height()

        self.createFont("N", "dejavusansmono", 40, (400, 300 +
                                                    height), "Press M to go back", (255, 255, 255))

        # Keybinds
        self.createKeybind(pygame.K_m, self.go_to_level)
        self.createTimer("M Press2", 900)

        # Instances
        self.createInstance(Player("Player", (100, 100), 64, 64, (0, 0, 255)))
        self.createInstance(Block("Block", (100, 300), 64, 64, (255, 130, 70)))

    def go_to_level(self):
        """Go to the next level."""
        timer = self.getTimer("M Press2")

        if timer["done"] == True:
            self.game.switch_room("Titlescreen")
            self.resetTimer("M Press2")

    def update(self):
        """Update."""
        self.updateRoom()
