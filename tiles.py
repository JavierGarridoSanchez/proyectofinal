import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        # le decimos a la clase que tamaño de superficie tendrá (x , y)
        self.image = pygame.Surface((size, size))
        # pone color
        self.image.fill('grey')
        # regoge el tamaño de la 'imagen'
        # y con el atributo 'topleft' hacemos que
        # aparezca desde la posicion indicada
        self.rect = self.image.get_rect(topleft=pos)

    # movimiento de la camara ficticia porque pygame no tine camara (movimiento de cacda valdosa)
    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift
