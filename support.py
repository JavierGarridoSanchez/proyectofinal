from csv import reader
import pygame
from settings import tile_size
from os import walk


# importamos las imagenes de una carpeta porque son animadas,
# asi podremos ir pasandolas para refrescarla
def import_folder(path):
    surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


# recorta la imagen del terrenno estando en una misma imagen
def import_cut_graphics(path):
    # recojo la img, y le quito los negros
    surface = pygame.image.load(path).convert_alpha()
    # recojo el ancho y el alto,  y le dividimos el tamaño de la baldosa
    # sacmos el ancho de la imagen
    tile_num_x = int(surface.get_size()[0] / tile_size)
    # sacamos el alto de la img
    tile_num_y = int(surface.get_size()[1] / tile_size)
    # lo que hicimos hasta ahora es pillar el primer bloque de 64 de la imagen.

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            # CON ESTO CREAMOS UNA SUPERFICIE PARA CADA TILE Y LE VAMOS METIENDO EN UN ARRAY,
            # LO ULTIMO PARA QUITAR EL NEGRO RESTANTE
            new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles
