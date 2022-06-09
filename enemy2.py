import level
from enemy import Enemy
from random import randint
import time


class Enemy2(Enemy):
    def __init__(self, size, x, y, current_level):
        self.current_level = current_level
        self.path = 'graphics/enemy/run2'
        self.random = None
        super().__init__(size, x, y, self.path)

    def move(self):
        self.rect.x += self.speed
        self.random = randint(-2, 2)
        if self.current_level == 1:
            self.rect.y += self.speed
            self.rect.x += self.random


        # esto es para recolocar el personaje centrado en el suelo porque flota un poco por la imagen,
        # por lo que bajo la parte de la imagen con el 1 que seria la y
