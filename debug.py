import pygame

pygame.init()
font = pygame.font.Font(None, 30)


def debug(info, y=10, x=10):
    pantalla = pygame.display.get_surface()
    datos = font.render(str(info), True, 'Black')
    datos_rect = datos.get_rect(topleft=(x, y))
    pantalla.blit(datos, datos_rect)
