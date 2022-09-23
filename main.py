import pygame, sys
from pytmx.util_pygame import load_pygame

from player import Player
from settings import *
from level import Level


class Game:
    def __init__(self):
    # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.level = Level(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     self.level.create_bullet()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()




