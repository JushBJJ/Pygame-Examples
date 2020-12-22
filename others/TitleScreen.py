"""Title Screen Test."""
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


class Room:
    """Room Class Template."""

    def __init__(self, name, **kwargs):
        """Initialize."""
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.bgColor = (0, 0, 0)
        self.screen = pygame.display.get_surface()
        self.instances = pygame.sprite.Group()
        self.fonts = dict({})
        self.keybinds = dict({})
        self.clocks = dict({})

        for name, value in enumerate(kwargs):
            if hasattr(self, str(name)):
                setattr(self, name, value)

    def createFont(self, fontName, fontType, fontSize, fontPosition, fontText, fontColor, show=True):
        """Create new font object.

        Args:
            fontName (string): Name of the font. (Example: "Jerry")
            fontType (string): Font type. (Example: "UbuntuMono")
            fontSize (int): Size of the font.
            fontPosition (tuple): (x,y) position of the font.
            fontText (string): Content of the font.
            fontColor (tuple): (R,G,B) color of the font.
            show (bool): Toggle whether to show font or not.
        """
        fontPath = pygame.font.match_font(fontType)
        self.fonts[fontName] = {
            "object": pygame.font.Font(fontPath, fontSize),
            "text": fontText,
            "color": fontColor,
            "position": fontPosition,
            "show": True
        }

    def updateFont(self, font, fontText, fontColor, fontPosition):
        """Update individual font.

        Args:
            font (class<pygame.font.Font>): Font class.
            fontText (string): Font content.
            fontColor (tuple): (R,G,B) color of the font.
            fontPosition (tuple): (x,y) position of the font.
        """
        surface = font.render(fontText, False, fontColor)
        rect = surface.get_rect(center=(fontPosition[0], fontPosition[1]))

        self.screen.blit(surface, rect)

    def checkKeybinds(self):
        """Check if key in the keybinds dictionary is pressed and run function if so."""
        keys = pygame.key.get_pressed()

        for key in self.keybinds.keys():
            if keys[int(key)]:
                self.keybinds[key]()  # Trigger function

    def createKeybind(self, key, function):
        """Create keybind for the room to trigger a function.

        Args:
            key (int): Key that will be used to trigger the function
            function (method): Function to be run.
        """
        self.keybinds[str(key)] = function

    def getTimer(self, name):
        """
        Return the timer by its name.

        Args:
            name (string): Name of the timer

        Returns:
            pygame.clock.Clock(): Clock object.
        """
        return self.clocks[name]

    def resetTimer(self, name):
        """
        Reset the selected timer.

        Args:
            name (string): Name of the timer.
        """
        if self.clocks[name]["done"] == True:
            # Reset Time and Done values
            self.clocks[name]["time"] = 0
            self.clocks[name]["done"] = False

    def updateTimers(self):
        """Update every timer in the dictionary."""
        for clock in self.clocks.keys():
            if self.clocks[clock]["done"] == False:
                # Tick the clock
                self.clocks[clock]["clock"].tick(60)

                # Increment time
                self.clocks[clock]["time"] += self.clocks[clock]["clock"].get_time()

                # Check if clock has reached the goal.
                time = self.clocks[clock]["time"]
                milliseconds = self.clocks[clock]["milliseconds"]

                if time > milliseconds:
                    # Timer done
                    self.clocks[clock]["done"] = True

    def createTimer(self, name, milliseconds):
        """
        Create a new timer.

        Args:
            name (string): Name of the timer.
            milliseconds (int): Time till the timer stops.
        """
        self.clocks[name] = {
            "clock": pygame.time.Clock(),
            "milliseconds": milliseconds,
            "time": 0,
            "done": True
        }

    def updateRoom(self):
        """Update room."""
        self.screen.fill(self.bgColor)

        for name in self.fonts.keys():
            font = self.fonts[name]
            if font["show"]:
                self.updateFont(font["object"], font["text"],
                                font["color"], font["position"])

        self.updateTimers()
        self.instances.update()
        self.checkKeybinds()


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

    def go_to_level(self):
        """Go to the next level."""
        timer = self.getTimer("M Press2")

        if timer["done"] == True:
            self.game.switch_room("Titlescreen")
            self.resetTimer("M Press2")

    def update(self):
        """Update."""
        self.updateRoom()


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))

done = False

game = Game()

# Titlescreen
room = game.add_room(Titlescreen(game))

# Level 1
room = game.add_room(Level1(game))

# Game
game.switch_room("Titlescreen")


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    game.update()
    pygame.display.flip()

pygame.quit()
