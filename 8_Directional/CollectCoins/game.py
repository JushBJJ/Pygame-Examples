"""Game."""
import pygame


class Game:
    """Game Class that stores every level."""

    def __init__(self):
        """Initialize."""
        self.rooms = pygame.sprite.Group()
        self.currentRoom = None

    def add_room(self, room):
        """Add a room into the sprite group.

        Args:
            room (class(pygame.sprite.Sprite)): Contains essential room information.

        Returns:
            class<room>: Room object
        """
        self.rooms.add(room)
        return room

    def get_room(self, name):
        """
        Return the room given by the name.

        Args:
            name (string): The name of the room.

        Returns:
            class<room>: The room object
        """
        for room in self.rooms:
            if room.name == name:
                return room

    def switch_room(self, name):
        """Switch to room (using name).

        Args:
            name (string): Name of the room.
        """
        for room in self.rooms:
            if room.name == name:
                self.currentRoom = room

        return self.currentRoom

    def update(self):
        """Update current room."""
        self.currentRoom.update()
