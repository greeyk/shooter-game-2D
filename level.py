import pygame
from settings import *
from support import *
from tile import Tile
from player import Player
from bullet import Bullet
from debug import debug

bullets = []

class Level:
    def __init__(self, screen):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.screen = screen

        # sprite grroup setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()


    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.screen)

    def create_bullet(self):
        x, y = pygame.mouse.get_pos()
        player_x = self.player.rect.x - self.visible_sprites.offset.x + 16
        player_y = self.player.rect.y - self.visible_sprites.offset.y + 16
        b = Bullet(player_x, player_y, 5, 5, 15, x, y)
        bullets.append(b)

    def draw_bullet(self):
        for b in bullets:
            b.move()
        for b in bullets:
            b.draw(self.display_surface)


    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.display_surface
        self.draw_bullet()
        debug(self.player.direction)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # general setup
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating floor
        self.floor_surf = pygame.image.load('graphics/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)







