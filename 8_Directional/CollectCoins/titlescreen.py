"""Titlescreen."""
import pygame
from room import *


class Titlescreen(pygame.sprite.Sprite, Room):
    """Title screen of the game."""

    def __init__(self, game):
        """
        Initialize the room.

        Args:
            game (class<game>): Game class
        """
        pygame.sprite.Sprite.__init__(self)
        Room.__init__(self, "Titlescreen")
        self.game = game

        # Text
        self.createFont("Title", "dejavusansmono", 50, (400, 300),
                        "Titlescreen", (255, 255, 255))

        height = self.fonts["Title"]["object"].get_height()

        self.createFont("N", "dejavusansmono", 40, (400, 300+height),
                        "Press N to go to next level.", (255, 255, 255))

        # Keybinds
        self.createKeybind(pygame.K_n, self.go_to_level)
        self.createTimer("N Press1", 900)

    def go_to_level(self):
        """Go to the next level."""
        timer = self.getTimer("N Press1")

        if timer["done"] == True:
            self.game.switch_room("Level1")
            self.resetTimer("N Press1")

    def update(self):
        """Update."""
        self.updateRoom()
