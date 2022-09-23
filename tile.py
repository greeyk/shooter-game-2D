import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((tile_size, tile_size))):
        super().__init__(groups)
        self.pos = pos
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=pos)
        elif sprite_type == 'shot':
            self.rect = self.image.get_rect(center=pos)
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -30)