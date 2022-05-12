import pygame
from tiles import Tile
from setings import tile_size, screen_width
from player import Player


class Level:
    def __init__(self, level_data, surface):
        # level set up
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    """layout  = level_data"""
    def setup_level(self, layout):

        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                # x e y son la posición en la que se posicionarán los objetos que leamos
                x = col_index * tile_size
                y = row_index * tile_size

                # que hay en cada celda
                if cell == 'X':
                    # que representa en el mapa
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)

                if cell == 'P':
                    # x e y son la posición de la valdosa
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def scroll_x(self):
        # recogemos el personaje, su posicion en el eje x y su dirección
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        # comprobamos la posicion del jugador,
        # 'direction_x', és el vector de dirección del
        # jugador que incrementa cuando apretamos las
        # teclas, al dejarlas de pulsar en una dirección
        # y pulsar en otra, estamos declarando la intención
        # de nuestro jugador de movernos en esa otra dirección.
        # al dejar de pulsarlas devuelve la velocidad
        # a nuestro personaje y la elimina de el mundo
        # dando así la sensación de movimiento de camara

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        # player
        self.player.update()
        self.player.draw(self.display_surface)
        self.scroll_x()
