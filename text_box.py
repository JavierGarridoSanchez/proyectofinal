import pygame
from main_menu import FONT
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


class InputBox:

    def __init__(self, x, y, w, h, text='Player Name'):
        self.rect = pygame.Rect(x, y, w, h + 10)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.screen = pygame.display.get_surface()

    def evento_manipulacion(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # si el usuario clica en el la caja de texto.
            if self.rect.collidepoint(event.pos):
                # pasa de inactivo a activo
                self.active = not self.active
                self.text = ''
            else:
                self.active = False
                if self.text == '':
                    self.text = 'Player Name'
            # cambia el color actual de la caja de texto.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Volver a renderizar el texto
        self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Aumenta le tamaño de la caja si el texto es demasiado largo.
        self.rect.w = max(200, self.txt_surface.get_width()+10)

    def draw(self, screen):
        # inserta el texto
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # inserta el rectangulo
        pygame.draw.rect(screen, self.color, self.rect, 2)
