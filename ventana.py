import pygame
import sys
import Personaje
pygame.init()

SIZE = (800, 500)

screen = pygame.display.set_mode(SIZE)

personaje = Personaje(screen.)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
