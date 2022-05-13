import pygame
from tiles import Tile
from setings import tile_size, screen_width, screen_height
from player import Player


class Level:
    def __init__(self, level_data, surface):
        # level set up
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift_x = 0
        self.world_shift_y = 0

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
            self.world_shift_x = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift_x = -8
            player.speed = 0
        else:
            self.world_shift_x = 0
            player.speed = 8

    def scroll_y(self):
        # recogemos el personaje, su posicion en el eje x y su dirección
        player = self.player.sprite
        player_y = player.rect.centerx
        direction_y = player.direction.y

        # comprobamos la posicion del jugador,
        # 'direction_x', és el vector de dirección del
        # jugador que incrementa cuando apretamos las
        # teclas, al dejarlas de pulsar en una dirección
        # y pulsar en otra, estamos declarando la intención
        # de nuestro jugador de movernos en esa otra dirección.
        # al dejar de pulsarlas devuelve la velocidad
        # a nuestro personaje y la elimina de el mundo
        # dando así la sensación de movimiento de camara

        if player_y < screen_height / 4 and direction_y < 0:
            self.world_shift_y = 8
            player.speed = 0
        elif player_y > screen_height - (screen_height / 4) and direction_y > 0:
            self.world_shift_y = -8
            player.speed = 0
        else:
            self.world_shift_y = 0
            player.speed = 8

    # detecta la colisión en el eje x
    def horitzontal_colision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_colision(self):
        player = self.player.sprite
        player.apply_gravity()

        # si se detecta la colision entre una valdosa y
        # un jugador comprobamos si la direccion en la
        # que se quiere mover el jugador en el eje y es
        # positiva o negativa (abajo o arriba),
        # ponemos la parte de abajo del jugador en la
        # misma posición que la parte de arriba de la valdosa

        for sprite in self.tiles.sprites():
            if player.rect.colliderect(sprite.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    # para evitar que el personaje atraviese la parte de arriba ni se pegue al techo
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def run(self):
        self.tiles.update(self.world_shift_x)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        # self.scroll_y()

        # player
        self.player.update()
        self.horitzontal_colision()
        self.vertical_colision()
        self.player.draw(self.display_surface)


