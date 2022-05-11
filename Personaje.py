import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, pantalla, x, y):
        super().__init__()
        self.speed_x = 0
        self.image = pygame.image.load("imgs/run1-izq.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0
        self.speed_x = 0
        self.img_derecha = [pygame.image.load('imgs/run1.png'),
                 pygame.image.load('imgs/run2.png'),
                 pygame.image.load('imgs/run3.png'),
                 pygame.image.load('imgs/run4.png'),
                 pygame.image.load('imgs/run5.png'),
                 pygame.image.load('imgs/run6.png')]
        self.img_izquierda = [pygame.image.load('imgs/run1-izq.png'),
                   pygame.image.load('imgs/run2-izq.png'),
                   pygame.image.load('imgs/run3-izq.png'),
                   pygame.image.load('imgs/run4-izq.png'),
                   pygame.image.load('imgs/run5-izq.png'),
                   pygame.image.load('imgs/run6-izq.png')]
        self.img_salto = [pygame.image.load('imgs/jump1.png'), pygame.image.load('imgs/jump2.png')]
        self.pasos = 0
        self.izquierda = False
        self.salto = False

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5

        if keystate[pygame.K_UP] and not self.salto :


        self.rect.x += self.speed_x
        if self.rect.right > pantalla.:
            self.rect.right = W
        if self.rect.left < 0:
            self.rect.left = 0

    def actualiza_movimiento(self, pantalla):
        if self.speed_x + 1 >= 6:
            self.speed_x = 0

        if not self.derecha:
            pantalla.blit(self.img_izquierda[self.pasos // 1], (int(px), int(py)))
            self.pasos += 1

