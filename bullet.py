import pygame, math, random

from settings import tile_size, screen_width, screen_height
from tile import Tile


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, targetx, targety, groups, tiles, player):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/flame.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.display_surface = pygame.display.get_surface()
        self.targetx = targetx
        self.targety = targety

        # collision
        self.tiles = tiles
        self.shot_sprites = pygame.sprite.Group()
        self.player = player
        self.old_x = self.rect.x
        self.old_y = self.rect.y
        self.shot_x = self.player.x
        self.shot_y = self.player.y

        angle = math.atan2(self.targety - y, self.targetx - x)  # get angle to target in radians
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

    def wall_collision_logic(self):
        diff_x = self.rect.x - self.old_x
        diff_y = self.rect.y - self.old_y

        self.shot_x += diff_x
        self.shot_y += diff_y

        self.old_x = self.rect.x
        self.old_y = self.rect.y

    def wall_collision(self):
        # print('difff', diff_x, diff_y)
        # print(self.shot_x , self.shot_y)
        Tile((self.shot_x, self.shot_y), self.shot_sprites, 'shot')
        # for shot in self.shot_sprites:
        collision = pygame.sprite.groupcollide(self.shot_sprites, self.tiles, False, False)
        if collision:
            self.kill()

    def draw(self):
        if 0 <= self.rect.x <= screen_width and 0 <= self.rect.y <= screen_height:
            self.display_surface.blit(self.image, self.rect)
        else:
            self.kill()

        # print(self.x, self.y)

    def update(self):
        # self.collision()
        self.wall_collision_logic()
        self.move()
        self.draw()


