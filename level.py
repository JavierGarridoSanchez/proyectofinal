import pygame, sys
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height
from enemy import Enemy
from tiles import Tile, StaticTile, Crate, AnimatedTile, Coin, Palm
from decoration import Sky, Water, Clouds


class Level:
    def __init__(self, level_data, surface):

        # general
        self.display_surface = surface
        self.world_shift = -5

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # terrain
        # terrain es el nombre de la capa
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # cesped grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # coins
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
        self.clouds = Clouds(400,level_width,100)

        # decoration
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)

        # health barr
        self.current_health = 1000
        self.max_health = 1000
        self.health_bar_length = 100
        self.health_ratio = self.max_health / self.health_bar_length

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    print('player goes here')

                if val == '1':
                    hat_surface = pygame.image.load('graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        global sprite

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/terrain/terrain_tiles.png')
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
                        if val == '0': sprite = Coin(tile_size, x, y, 'graphics/coins/gold')
                        if val == '1': sprite = Coin(tile_size, x, y, 'graphics/coins/silver')

                    if type == 'fg palms':
                        if val == '0':  sprite = Palm(tile_size, x, y, 'graphics/terrain/palm_small', 38)
                        if val == '1': sprite = Palm(tile_size, x, y, 'graphics/terrain/palm_large', 64)

                    if type == 'bg palms':
                        sprite = Palm(tile_size, x, y, 'graphics/terrain/palm_bg', 64)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def run(self):

        #sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface,self.world_shift)

        # decoration
        self.sky.draw(self.display_surface)

        # back palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

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
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)
