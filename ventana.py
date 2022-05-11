import pygame
import sys
pygame.init()

SIZE = (800, 500)

screen = pygame.display.set_mode(SIZE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
