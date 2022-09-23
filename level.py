import pygame
from settings import *
from support import *
from tile import Tile
from player import Player
from bullet import Bullet
from debug import debug

class Level:
    def __init__(self, screen):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.screen = screen

        # sprite grroup setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.bullets = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        layouts = {'water': import_csv_layout("csv/map_water.csv"),
                   'lava': import_csv_layout('csv/map_lava.csv'),
                   'object': import_csv_layout('csv/map_objects.csv')
                   }
        graphics = {'objects': import_folder('graphics/objects')
                    }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * tile_size
                        y = row_index * tile_size
                        if style == 'water':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'lava':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            t = Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                            self.tile_sprites.add(t)


        self.player = Player((2400, 1800), [self.visible_sprites], self.obstacle_sprites, self.create_attack)

    def create_attack(self):
        x, y = pygame.mouse.get_pos()
        player_x = self.player.hitbox.x - self.visible_sprites.offset.x + 8
        player_y = self.player.hitbox.y - self.visible_sprites.offset.y + 8

        bullet = Bullet(player_x, player_y, 20, x, y, [self.visible_sprites], self.tile_sprites, self.player.hitbox)
        self.bullets.add(bullet)
        # print(x, y)
        # print('player pos:', player_x, player_y)

    def bullet_collision(self):
        if self.create_attack:
            for bullet in self.bullets:
                bullet.wall_collision()


    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.bullet_collision()
        self.visible_sprites.update()
        debug(self.player.hitbox)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # general setup
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating floor
        self.floor_surf = pygame.image.load('graphics/big_ground.png').convert()
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







