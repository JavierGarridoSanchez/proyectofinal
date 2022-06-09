import pygame, sys
import time

from scoreboard_dao_imple import ScoreBoardDaoImple

from support import import_csv_layout, import_cut_graphics, import_folder
from settings import tile_size, screen_height, screen_width
from enemy import Enemy
from enemy2 import Enemy2
from tiles import Tile, StaticTile, Crate, AnimatedTile, Coin, Palm
from decoration import Sky, Water
from player import Player
from ui import UI
from scoreboard import ScoreBoard
from game_data import levels_files, img_lvl_tile
from dao_manager import DaoManager


# import menu


class Level:
    def __init__(self, level_data, surface, name_jugador, img_lvl, current_level):
        self.level_data = level_data
        self.surface = surface

        self.path = 'graphics/enemy/run'

        # level_data = niveles[current_level]
        self.fuente = pygame.font.Font(None, 20)
        self.no_return = False  # para que solo entre al win una vez.
        self.current_level = current_level

        # general
        self.display_surface = surface
        self.world_shift = -1
        self.current_x = None

        # image tile change
        self.img_lvl = img_lvl

        # user interface
        self.ui = UI(surface)

        # sonido
        self.coin_sound = pygame.mixer.Sound('audio/effects/coin.wav')
        self.stomp_sound = pygame.mixer.Sound('audio/effects/stomp.wav')
        self.level_music_bg = pygame.mixer.Sound('audio/level_music.wav')
        self.level_music_bg.set_volume(0.2)

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        # le pasamos el parametro para cambiar la vida
        self.player_setup(player_layout, self.change_health)
        self.player_sprite = None

        # terrain
        # terrain es el nombre de la capa
        terrain_layout = import_csv_layout(level_data['terrain'])
        # le pasas la basura de datos, y la capa y iras al crear tile group
        # e iras recortando con el metodo cut la imagen para dividirla en 64px.
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        # cesped grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        # crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')
        # coins capas
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')
        # palmeras
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')
        # backround palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')
        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
        # constraints
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')
        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)
        # decoration
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)

        # vida
        self.max_health = 50
        self.cur_health = 50

        # coins
        self.coins = 0

        # puntuaciones y base de datos
        self.num_enemys_death = 0
        self.score_per_enemy = 0

        # nombre jugador
        self.name = name_jugador

        # final muerte
        self.death = False

        # fianl terminado
        self.end = False

        # llegas a la meta
        self.wins = False

        # indice para cambiar de nivel
        self.index = 1

        # guardar puntuaciones boolean
        self.save_points = True

        # base de datos DAO
        self.dao_manager = DaoManager()

        self.scoreboard = None
        self.bd = None

        self.level_music_bg.play(loops=-1)

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    self.player_sprite = Player((x, y), self.display_surface, change_health)
                    # añado el sprite del jugador
                    self.player.add(self.player_sprite)

                if val == '1':
                    hat_surface = pygame.image.load('graphics/character/hat.png').convert_alpha()
                    self.player_sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(self.player_sprite)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        global sprite
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(self.img_lvl)
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    # este no tendria que cortarlo ya que esta solo en un sprite
                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    # el orden de imagenes las pillas con la lista,
                    # pues si la imagen de la moneda plateada es la segunda,
                    # sera el 1, y mostaras la adecuada
                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size, x, y, 'graphics/coins/gold', 1)
                        if val == '1': sprite = Coin(tile_size, x, y, 'graphics/coins/red', 5)

                    if type == 'fg palms':
                        if val == '0':  sprite = Palm(tile_size, x, y, 'graphics/terrain/palm_small', 38)
                        if val == '1': sprite = Palm(tile_size, x, y, 'graphics/terrain/palm_large', 64)

                    if type == 'bg palms':
                        sprite = Palm(tile_size, x, y, 'graphics/terrain/palm_bg', 64)

                    if type == 'enemies':
                        if self.current_level == 1:
                            sprite = Enemy2(tile_size, x, y, self.current_level)
                        else:
                            sprite = Enemy(tile_size, x, y, 'graphics/enemy/run')

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    # detecta la colisiÃ³n en el eje x
    def horitzontal_colision(self):
        # nota he cambiado los rect de player por collision_rect para que tenga en cuenta la colision con la espada.
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        # ahora le decimos con que sprites queremos que el player colisione
        for sprite in self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                # si nos movemos a la izq
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                    # comprobamos que si el lado derecho esta mas alla del muro,
                    # si el lado derecho del jugador esta mas
                    # alla de el muro, entoneces el jugador ya no esta tocando ese muro derecho,
                    # vamos que comprobamos el punto de colision
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        # esto ahora mismo no lo necesito porque el rectangulo es estatico,
        # ya no que hay que actualizar el punto de origen
        # if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
        #     player.on_left = False
        #
        # if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
        #     player.on_right = False

    def change_health(self, amount):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0 or self.player.sprite.rect.top >= screen_height:
            # aqui hay que poner la pantalla nueva,
            # recoger los datos para la base de datos
            # y el cirre del juego para llevarlo al menú
            self.cur_health = 0
            # self.coins = 0
            self.end = True
            self.death = True
            self.level_music_bg.stop()
            time.sleep(1)

            # menu.main_menu()
            # self.display_surface.fill('black')

            # screen.fill('black')

    def check_win(self):
        # si colisiona la bandera final con el perso, terminamos
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False) and not self.no_return:
            self.current_level += 1
            self.save_scores()
            self.final = True
            self.wins = True
            self.level_music_bg.stop()
            time.sleep(1)

    def check_coin_collisions(self):
        # creamos una lista de colision  de monedas,
        # le pasamos el player para colisionar,
        # y queremos ver si colisiona con la  moneda y ponemos true para que desaparezca
        # (nota: se pone una lista porque puede pasar que en algunos casos hayan dos mendas juntas,
        # y las recojas a la vez, y claro no las procesaria como 2
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        # si las monedas colisionaron (osea si no esta vacio)
        if collided_coins:
            # sonido coin, si la pongo en el for sonaria 2 veces,
            # por ejemplo si cojo 2 monedas juntas.
            self.coin_sound.play()
            for coin in collided_coins:
                # sumamos cada coin
                self.coins += coin.value

    def check_crate_collisions(self):
        collided_powerup = pygame.sprite.spritecollide(self.player.sprite, self.crate_sprites, True)
        amount = 20
        if collided_powerup:
            self.coin_sound.play()
            for _ in collided_powerup:
                if 40 >= self.cur_health:
                    self.change_health(amount)
                if self.cur_health > 50:
                    self.cur_health = 50

    def vertical_colision(self):
        player = self.player.sprite
        player.apply_gravity()

        # si se detecta la colision entre una valdosa y
        # un jugador comprobamos si la direccion en la
        # que se quiere mover el jugador en el eje y es
        # positiva o negativa (abajo o arriba),
        # ponemos la parte de abajo del jugador en la
        # misma posiciÃ³n que la parte de arriba de la valdosa

        for sprite in self.terrain_sprites.sprites() + self.fg_palm_sprites.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:  # el personaje está cayendo
                    player.collision_rect.bottom = sprite.rect.top
                    # para evitar que el personaje atraviese la parte de arriba ni se pegue al techo
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:  # el personaje está subiendo (en el momento en el que saltas)
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        # si el jugador esta saltando o cayendo, o esta en el piso,
        # entonces ya no puiede estar en el piso
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        # verifico si el jugadoir comienza caerse de nuevo
        # if player.on_ceiling and player.direction.y > 0.1:
        #     player.on_ceiling = False

    def scroll_x(self):
        # recogemos el personaje, su posicion en el eje x y su direcciÃ³n
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        # comprobamos la posicion del jugador,
        # 'direction_x', Ã©s el vector de direcciÃ³n del
        # jugador que incrementa cuando apretamos las
        # teclas, al dejarlas de pulsar en una direcciÃ³n
        # y pulsar en otra, estamos declarando la intenciÃ³n
        # de nuestro jugador de movernos en esa otra direcciÃ³n.
        # al dejar de pulsarlas devuelve la velocidad
        # a nuestro personaje y la elimina de el mundo
        # dando asÃ­ la sensaciÃ³n de movimiento de camara

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def check_enem_colisions(self):
        # primero de nada tengo que saber cuantos enemigos estoy chocando
        # en false porque no siempre queremos k el enemigo desaparezca,
        # ya que cuando el player le toque estando a su izq o dere,
        # se supone que el enemigo no muere.
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        # si colisiona
        if enemy_collisions:
            # revisamos todos los enemigos
            for enemy in enemy_collisions:
                # obtengo el centro del enemigo
                enemy_center = enemy.rect.centery
                # obtengo la parte superior del enemigo
                enemy_top = enemy.rect.top
                # obtengo la parte inferior del player
                player_bottom = self.player.sprite.rect.bottom
                # si la parte superior del enemigo, es inferior a la del player,
                # y si eso es mas pequeño que el centro del enemigo
                # y ademas si el personaje esta cayendo al suelo,
                # ya que si no hicieras eso,
                # el personaje cerca del enemigo podria saltar y matar al enemigo antes de caer y topar con el,
                # ya que estaria en el rango del rectangulo del enemigo
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -18  # para que salte al golpearle
                    self.num_enemys_death += 1
                    self.score_per_enemy += 2
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def save_scores(self):
        self.no_return = True
        self.bd = self.dao_manager.get_dao_markers()
        lista = [self.name, self.score_per_enemy, self.num_enemys_death, self.coins, self.current_level]
        jug = self.bd.read_player(lista[0])
        self.scoreboard = ScoreBoard(self.name, self.score_per_enemy, self.num_enemys_death, self.coins,
                                     self.current_level)
        if jug is not None:
            listado_jugador = []

            for x in jug:
                listado_jugador.append(x)
            sum_coins = listado_jugador[3] + self.coins
            sum_score_por_enemys = listado_jugador[1] + self.score_per_enemy
            sum_enemies_death = listado_jugador[2] + self.num_enemys_death

            if self.current_level > len(levels_files) - 1:
                lista = [self.name, sum_score_por_enemys, sum_enemies_death, sum_coins, self.current_level]
                self.scoreboard.score = lista[1]
                self.scoreboard.kills = lista[2]
                self.scoreboard.coins = lista[3]
                # marcadores.level = lista[4]

            self.bd.delete_player(lista[0])

        self.bd.insert_player(self.scoreboard)

    def run(self):

        # sky
        self.sky.draw(self.display_surface)

        # decoration
        self.sky.draw(self.display_surface)

        # back palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # goal
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # tierra
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # enemics
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # foreground
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # player
        self.player.update()
        self.horitzontal_colision()
        self.vertical_colision()
        self.scroll_x()
        self.player.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)

        # salud
        # le pasamos la vida actual y la completa
        self.ui.show_health(self.cur_health, self.max_health)

        # mostrar cantidad de monedas monedas
        self.ui.show_coins(self.coins)
        # chekear la colision de las monedas
        self.check_coin_collisions()
        self.check_crate_collisions()

        # colision enemigos
        self.check_enem_colisions()

        # self.guardar_puntuaciones()

        # self.guardar_puntuaciones()

        # validacion salida
        self.check_win()

        # game over
        self.check_game_over()
