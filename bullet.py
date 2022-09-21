import pygame, math, random

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, targetx, targety, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/flame.png')
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(0, 0)
        self.display_surface = pygame.display.get_surface()

        angle = math.atan2(targety - y, targetx - x)  # get angle to target in radians
        print('Angle in degrees:', int(angle * 180 / math.pi))
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.x = x
        self.y = y

    # Override
    def move(self):
        # self.x and self.y are floats (decimals) so I get more accuracy
        # if I change self.x and y and then convert to an integer for
        # the rectangle.
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self):
        self.display_surface.blit(self.image, self.rect)
