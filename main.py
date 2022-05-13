import pygame
import sys
from setings import *
from level import Level
from tiles import Tile


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
# tile_prove = pygame.sprite.Group(Tile((100, 100), 200))
level = Level(level_map, screen)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    # tile_prove.draw(screen)
    level.run()

    pygame.display.update()
    clock.tick(60)

