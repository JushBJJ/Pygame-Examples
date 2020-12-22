"""Pygame Template with Collision."""
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

    def __init__(self, x, y, width, height, color, name="Rectangle"):
        """Creation of Rectangle."""
        Sprite.__init__(self, x, y, width, height, color, name)
        # There can be multiple instances of the same class
        Rect.instances.add(self)
        self.solid = True

    def update(self):
        """Update Function."""
        print(f"Updated {self.name}")


class Player(Sprite):
    """Player Sprite Class."""

    # Can be used for multiple levels, saves, and more
    instances = pygame.sprite.Group()

    def __init__(self, x, y, width, height, color, name="Player"):
        """Init for player class."""
        Sprite.__init__(self, x, y, width, height, color, name)
        Player.instances.add(self)

        # Speed of the player
        self.speed = 5

        # Movement Controls
        self.keys_movement = {
            str(pygame.K_w): (0, -self.speed, "up"),
            str(pygame.K_a): (-self.speed, 0, "left"),
            str(pygame.K_s): (0, self.speed, "down"),
            str(pygame.K_d): (self.speed, 0, "right")

        }

        self.direction = "right"
        self.shootTimer = pygame.time.Clock()
        self.time = 0

    def collision(self):
        """Collision."""
        collisions = pygame.sprite.spritecollide(self, Sprite.Sprites, False)
        # collisions[x] returns a rectangle class/Sprite class

        # spritecollide also contains the player itself
        # so if it touches another sprite, it must have more than 1
        if len(collisions) > 1:
            for collide in collisions:  # Loop through the list of collisions
                if hasattr(collide, "solid"):  # Check if sprite has solid attribute
                    if collide.solid == True:
                        self.rect.x = self.oldX
                        self.rect.y = self.oldY

        self.oldX = self.rect.x
        self.oldY = self.rect.y

    def movement(self):
        """Movement."""
        keys = pygame.key.get_pressed()

        for key in self.keys_movement.keys():
            if keys[int(key)] == 1:
                self.rect.x += self.keys_movement[key][0]
                self.rect.y += self.keys_movement[key][1]
                self.direction = self.keys_movement[key][2]
                break  # Break here to disable diagonal movement that messes up collision

    def shoot(self):
        """Shooting."""
        # 90ms shooting delay
        if self.time >= 90:
            self.time = 0
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                # Create Bullet
                Projectile(self.rect.x + (self.rect.width / 2),
                           self.rect.y+(self.rect.height/2),
                           10, 10, (255, 255, 255), "Bullet", self.direction)
        else:
            self.time += self.shootTimer.get_time()
            self.shootTimer.tick(60)

    def update(self):
        """Sequence of functions to update."""
        self.movement()
        self.collision()
        self.shoot()


class Projectile(Sprite):
    """Projectile Class."""

    instances = pygame.sprite.Group()

    def __init__(self, x, y, width, height, color, direction, name="Projectile"):
        """Projectile init."""
        Sprite.__init__(self, x, y, width, height, color, name)
        Projectile.instances.add(self)

        self.speed = 10
        self.direction = direction

        # self.posChange["example"]=(x change, y change)
        self.posChange = {
            "left": (-self.speed, 0),
            "right": (self.speed, 0),
            "down": (0, self.speed),
            "up": (0, -self.speed)
        }

    def update(self):
        """Keep Projectile Moving."""
        self.rect.x += self.posChange[self.direction][0]
        self.rect.y += self.posChange[self.direction][1]

        # Destroy bullet when out of screen
        if self.rect.x <= 0 or \
                self.rect.x >= pygame.display.get_window_size()[0]:
            Projectile.instances.remove(self)
            Sprite.Sprites.remove(self)
            print("Destroyed Bullet")
        elif self.rect.y <= 0 or \
                self.rect.y >= pygame.display.get_window_size()[1]:
            Projectile.instances.remove(self)
            Sprite.Sprites.remove(self)
            print("Destroyed Bullet")


# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600), vsync=True)
clock = pygame.time.Clock()

# Creating Objects
rect1 = Rect(400, 300, 100, 100, (0, 255, 0))
rect2 = Player(200, 400, 100, 100, (255, 0, 0))

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

    print(clock.get_fps())

# Quit
pygame.quit()
