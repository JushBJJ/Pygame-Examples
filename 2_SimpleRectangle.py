"""Simple Pygame Template with Rectangles."""
import pygame

# Objects


class Sprite(pygame.sprite.Sprite):
    """Sprites Folder."""

    Sprites = pygame.sprite.Group()

    def __init__(self, x, y, width, height, color):
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


class Rect(Sprite):
    """Simple Rectangle Base Class."""

    group = pygame.sprite.Group()

    def __init__(self, x, y, width, height, color):
        """Creation of Rectangle."""
        pygame.sprite.Sprite.__init__(self)
        Sprite.__init__(self, x, y, width, height, color)
        Rect.group.add(self)


# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600), vsync=True)
clock = pygame.time.Clock()

# Creating Objects
rect1 = Rect(100, 100, 100, 100, (0, 255, 0))
rect2 = Rect(200, 400, 100, 100, (255, 0, 0))

# Game Loop
Running = True

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    # Draw all Sprites
    Sprite.Sprites.draw(screen)

    # Update Screen
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# Quit
pygame.quit()
