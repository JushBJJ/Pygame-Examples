"""Pygame Template with Rectangle Movement."""
import pygame

# Objects


class Sprite(pygame.sprite.Sprite):
    """Sprites Folder."""

    Sprites = pygame.sprite.Group()

    def __init__(self, x, y, width, height, color, name):
        """Creation of Sprite."""
        pygame.sprite.Sprite.__init__(self)
        Sprite.Sprites.add(self)

        self.image = pygame.surface.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height

        self.name = name


class Rect(Sprite):
    """Simple Rectangle Base Class."""

    instances = pygame.sprite.Group()

    def __init__(self, x, y, width, height, color, name):
        """Creation of Rectangle."""
        pygame.sprite.Sprite.__init__(self)
        Sprite.__init__(self, x, y, width, height, color, name)
        # There can be multiple instances of the same class
        Rect.instances.add(self)

    def update(self):
        """Update Function."""
        print(f"Updated {self.name}")


class Player(Sprite):
    """Player Sprite Class."""

    # Can be used for multiple levels, saves, and more
    instances = pygame.sprite.Group()

    def __init__(self, x, y, width, height, color, name):
        """Init for player class."""
        Sprite.__init__(self, x, y, width, height, color, name)
        Player.instances.add(self)

        self.keys_movement = {
            str(pygame.K_w): (0, -5),
            str(pygame.K_a): (-5, 0),
            str(pygame.K_s): (0, 5),
            str(pygame.K_d): (5, 0)

        }

    def movement(self):
        """Movement."""
        keys = pygame.key.get_pressed()

        for key in self.keys_movement.keys():
            if keys[int(key)] == 1:
                self.rect.x += self.keys_movement[key][0]
                self.rect.y += self.keys_movement[key][1]

    def update(self):
        """Sequence of functions to update."""
        self.movement()


# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600), vsync=True)
clock = pygame.time.Clock()

# Creating Objects
rect1 = Rect(100, 100, 100, 100, (0, 255, 0), "Rect1")
rect2 = Player(200, 400, 100, 100, (255, 0, 0), "Player1")

# Game Loop
Running = True

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    # Fill Screen Background
    screen.fill((0, 0, 0))

    # Update all Sprites
    Sprite.Sprites.update()

    # Draw all Sprites
    Sprite.Sprites.draw(screen)

    # Update Screen
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# Quit
pygame.quit()
