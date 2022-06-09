import pygame
import sys
from pygame.locals import *
from dao_manager import DaoManager

from level import Level
from game_data import img_lvl_tile, levels
from settings import *
import text_box

mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('Ninja x Kirby')
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
BACKROUND_MENU = pygame.image.load('imgs/fondomenu.png').convert()
BG_IMG = pygame.transform.scale(BACKROUND_MENU, (screen_width, screen_height))
BACKROUND_SCORE = pygame.image.load('graphics/FondoLejos.png').convert()
BG_SCORE = pygame.transform.scale(BACKROUND_SCORE, (screen_width, screen_height))

FONT = pygame.font.SysFont('Corbel', 30)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)


class MainMenu:
    def __init__(self):
        self.name_player = None
        self.DaoManager = DaoManager()
        self.bd = self.DaoManager.get_dao_markers()

    def draw_text(self, text, font, color, surface, x, y, draw_rect=False):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, textrect)
        if draw_rect:
            pygame.draw.rect(surface, COLOR_BLACK, textrect, 1)

    def end(self, level):
        text_wins = 'HAS GANADO!! Pulsa ESC para volver al menú'
        text_loose = 'HAS MUERTO! Pulsa ESC para volver al menú'
        running = True
        while running:
            screen.fill((0, 0, 0))
            if level.death:
                self.draw_text(text_loose, FONT, COLOR_WHITE, screen, screen_width / 2, screen_height / 2)
            elif not level.death:
                self.draw_text(text_wins, FONT, COLOR_WHITE, screen, 20, 20)
                self.game('')
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            mainClock.tick(60)

    def game(self, name_player):
        running = True

        player = self.bd.get_player_level(name_player)
        if player is not None:
            current_level = self.management_level(player[0])

        else:
            current_level = 0

        screen_game = pygame.display.set_mode((screen_width, screen_height))

        level = Level(levels[current_level], screen_game, name_player, img_lvl_tile[current_level], current_level)

        while running and not level.wins and not level.end:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        level.level_music_bg.stop()
                        running = False
            level.run()

            if level.wins:

                MainMenu()
                running = False
            elif level.end:
                self.end(level)
                running = False
            pygame.display.update()
            mainClock.tick(60)

    @staticmethod
    def management_level(player):
        current_level = 0
        if player is not None:
            current_level = player
        if player > len(levels) - 1:
            current_level = 0
        return current_level

    def score_view(self):
        running = True
        screen_score = pygame.display.set_mode((screen_width, screen_height))

        txt = 'Puntuaciones'
        heigth = 30
        screen_score.blit(BG_SCORE, (0, 0))
        self.draw_text(txt, FONT, COLOR_BLACK, screen, screen_width / 2, heigth)
        title = f' NOMBRE | PUNTUACIÓN | ENEMIGOS ELIMINADOS | PUNTUACIÓN DE MONEDAS '
        self.draw_text(title, FONT, COLOR_BLACK, screen_score, screen_width / 2, heigth + 30, True)
        heigth += screen_height / 5

        # leemos los jugadores que estn en la base de datos y los dibujo en la pantalla
        players = self.bd.top_players()
        for player in players:
            heigth += 35
            fila = f' {player[0]} | {player[1]} | {player[2]} | {player[3]} '
            self.draw_text(fila, FONT, COLOR_BLACK, screen_score, screen_width / 2, heigth)

        txt_info = 'Presiona ESC para volver al menú'
        self.draw_text(txt_info, FONT, COLOR_BLACK, screen_score,
                       screen_width - (len(txt_info) * len(txt_info) / 4.5), screen_height - 30)

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.flip()
            mainClock.tick(60)

    def main(self):

        posx_button = screen_width / 2
        posy_button = screen_height / 2
        button_width = 200
        button_height = 50
        button_1 = pygame.Rect(posx_button - (button_width / 2), posy_button, button_width, button_height)
        button_2 = pygame.Rect(posx_button - (button_width / 2), posy_button + 100, button_width, button_height)
        button_3 = pygame.Rect(posx_button - (button_width / 2), posy_button + 200, button_width, button_height)

        input_box = text_box.InputBox(100, 200, 140, 32)

        while True:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                input_box.evento_manipulacion(event)

                nombre_jugador = input_box.text
                if event.type == MOUSEBUTTONDOWN:
                    if button_1.collidepoint((mx, my)):
                        self.game(nombre_jugador)
                    if button_2.collidepoint((mx, my)):
                        # self.options()
                        pass
                    if button_3.collidepoint((mx, my)):
                        self.score_view()

            input_box.update()

            screen.blit(BG_IMG, (0, 0))

            pygame.draw.rect(screen, (33, 149, 156), button_1, 0, 0, 10, 50, 50, 10)
            pygame.draw.rect(screen, (33, 149, 156), button_2, 0, 0, 10, 50, 50, 10)
            pygame.draw.rect(screen, (33, 149, 156), button_3, 0, 0, 10, 50, 50, 10)

            self.draw_text('Ninja x Kirby', FONT, COLOR_WHITE, screen, screen_width / 2, screen_height / 5)
            self.draw_text('Jugar', FONT, COLOR_WHITE, screen, button_1.centerx, button_1.centery)
            self.draw_text('Opciones', FONT, COLOR_WHITE, screen, button_2.centerx, button_2.centery)
            self.draw_text('Puntuaciones', FONT, COLOR_WHITE, screen, button_3.centerx, button_3.centery)
            input_box.draw(screen)

            pygame.display.flip()
            mainClock.tick(60)


if __name__ == '__main__':
    menu = MainMenu()
    menu.main()
    pygame.quit()
