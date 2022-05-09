import pygame
import sys

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

from pygame.locals import *

W = 500
H = 500
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((W, H), 0, 32)
fondo = pygame.image.load("imgs/fondomenu.png").convert()  # aixo es perque s'optimitzi la img
bg_img = pygame.transform.scale(fondo, (W, H))

font = pygame.font.SysFont('Corbel', 20)
color = (255, 255, 255)


def draw_text(text, font, blue, surface, x, y):
    textobj = font.render(text, 1, blue)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


def main_menu():
    while True:

        screen.fill((0, 0, 0))
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)
        screen.blit(bg_img, (0, 0))

        mx, my = pygame.mouse.get_pos()
        # boton  = dibujar un rectangulo (widht, border_radius, )
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        button_3 = pygame.Rect(100, 500, 500, 100)

        text = font.render('quit', True, color)
        if button_1.collidepoint((mx, my)):
           # button_2 = pygame.draw.rect(screen, (33, 149, 156), button_3, 0, 0, 10, 50, 50, 10)

            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (33, 149, 156), button_1, 0, 0, 10, 50, 50, 10)
        pygame.draw.rect(screen, (33, 149, 156), button_2, 0, 0, 10, 50, 50, 10)
        #texto,fuente,color,pantalla,posicion x,y
        draw_text('Jugar', font, (255, 255, 255), screen, button_1.centerx - 20, button_1.centery - 10)
        draw_text('Opciones', font, (255, 255, 255), screen, button_2.centerx - 20, button_2.centery - 10)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


        pygame.display.update()
        mainClock.tick(60)


def game():
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('game', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('options', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


main_menu()
