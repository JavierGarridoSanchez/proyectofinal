import pygame
from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
    def __init__(self, size, x, y, path):
        self.path = path
        super().__init__(size, x, y, self.path)
        # esto es para recolocar el personaje centrado en el suelo porque flota un poco por la imagen,
        # por lo que bajo la parte de la imagen con el 1 que seria la y
        self.rect.y += size+10 - self.image.get_size()[1]
        self.speed = randint(3, 5)

    def move(self):
        self.rect.x += self.speed

    def flip_image(self):
        if self.speed > 0:
            # el primero es para invertir de derecha a izq, el segundo para abajo
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.flip_image()
