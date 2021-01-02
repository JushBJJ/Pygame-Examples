"""Room."""
import pygame
from PIL import Image


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

        for name, value in kwargs.items():
            if hasattr(self, str(name)):
                setattr(self, name, value)

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
        self.instances.draw(self.screen)
        self.checkKeybinds()

    # For AI

    def getInstance(self, name):
        """
        Get instance from name.

        Args:
            name (string): Name of the instance.

        Returns:
            sprite: Instance
        """
        for instance in self.instances:
            if instance.name == name:
                return instance

    def createInstance(self, instance):
        """
        Create a new instance.

        Args:
            instance (class): Class of the new instance.

        Returns:
            instance (class): Instance of the new instance
        """
        setattr(instance, 'instanceGroup', self.instances)
        self.instances.add(instance)
        return instance

    def removeInstance(self, instance):
        """
        Remove an instance.

        Args:
            instance (class): Class of the instance to remove.
        """
        self.instances.remove(instance)

    def createFont(self, fontName, fontType, fontSize, fontPosition, fontText, fontColor, show=True):
        """Create new font object.

        Args:
            fontName(string): Name of the font. (Example: "Jerry")
            fontType(string): Font type. (Example: "UbuntuMono")
            fontSize(int): Size of the font.
            fontPosition(tuple): (x, y) position of the font.
            fontText(string): Content of the font.
            fontColor(tuple): (R, G, B) color of the font.
            show(bool): Toggle whether to show font or not.
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
            font (class < pygame.font.Font >): Font class.
            fontText(string): Font content.
            fontColor(tuple): (R, G, B) color of the font.
            fontPosition(tuple): (x, y) position of the font.
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
            key(int): Key that will be used to trigger the function
            function(method): Function to be run.
        """
        self.keybinds[str(key)] = function

    def getTimer(self, name):
        """
        Return the timer by its name.

        Args:
            name(string): Name of the timer

        Returns:
            pygame.clock.Clock(): Clock object.
        """
        return self.clocks[name]

    def resetTimer(self, name):
        """
        Reset the selected timer.

        Args:
            name(string): Name of the timer.
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
            name(string): Name of the timer.
            milliseconds(int): Time till the timer stops.
        """
        self.clocks[name] = {
            "clock": pygame.time.Clock(),
            "milliseconds": milliseconds,
            "time": 0,
            "done": True
        }
