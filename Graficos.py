import pygame
import sys
from pygame.constants import QUIT
import time

# inici del pygame


pygame.init()
W = 1000
H = 600
FPS = 60
x = 0
y = 0
px = 50
py = 200
ancho = 40
velocidad = 5

# Música de fondo
pygame.mixer.music.load('sonido/intergalactic_odyssey.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.90)

# Control de FPS
clock = pygame.time.Clock()

# Variables salto
salto = False
# Contador de salto
cuentaSalto = 1

# Variables dirección
izquierda = False
derecha = False

# Pasos
cuentaPasos = 0

# pantalla i finestra
PANTALLA = pygame.display.set_mode((W, H))
pygame.display.set_caption("Juego")

# fons del joc
fondo = pygame.image.load("imgs/fondo.jpg").convert()  # aixo es perque s'optimitzi la img
fondo2 = pygame.image.load("imgs/fondomenu.png").convert()
bg_img = pygame.transform.scale(fondo, (W, H))
# Personaje
quieto = pygame.image.load('imgs/idle1.png')
rect = quieto.get_rect()
print(rect)

caminaDerecha = [pygame.image.load('imgs/run1.png'),
                 pygame.image.load('imgs/run2.png'),
                 pygame.image.load('imgs/run3.png'),
                 pygame.image.load('imgs/run4.png'),
                 pygame.image.load('imgs/run5.png'),
                 pygame.image.load('imgs/run6.png')]

caminaIzquierda = [pygame.image.load('imgs/run1-izq.png'),
                   pygame.image.load('imgs/run2-izq.png'),
                   pygame.image.load('imgs/run3-izq.png'),
                   pygame.image.load('imgs/run4-izq.png'),
                   pygame.image.load('imgs/run5-izq.png'),
                   pygame.image.load('imgs/run6-izq.png')]

salta = [pygame.image.load('imgs/jump1.png'),
         pygame.image.load('imgs/jump2.png')]

# Sonido
sonido_arriba = pygame.image.load('sonido/volume_up.png')
sonido_abajo = pygame.image.load('sonido/volume_down.png')
sonido_mute = pygame.image.load('sonido/volume_muted.png')
sonido_max = pygame.image.load('sonido/volume_max.png')


# Movimiento
def recargaPantalla():
    # Variables globales
    global cuentaPasos
    global x
    global y

    # Fondo en movimiento
    #     # obtenim el ample del fons, perque retorni "el resto"
    y_relativa = y % bg_img.get_rect().height
    #     # li restem el valor de y relativa - el ample del fons (li posem a la y perque es mogui arriba abaix)
    PANTALLA.blit(bg_img, (0, y_relativa - bg_img.get_rect().height))
    if y_relativa < W:
        PANTALLA.blit(bg_img, (0, y_relativa))
    # aqui es posa y que es perque agafara la posicio que li digui la y, per aixo aniras cambiant la x o la y
    y = y - 1
    # Contador de pasos
    if cuentaPasos + 1 >= 6:
        cuentaPasos = 0
    # Movimiento a la izquierda
    if izquierda:
        PANTALLA.blit(caminaIzquierda[cuentaPasos // 1], (int(px), int(py)))
        cuentaPasos += 1

        # Movimiento a la derecha
    elif derecha:
        PANTALLA.blit(caminaDerecha[cuentaPasos // 1], (int(px), int(py)))
        cuentaPasos += 1

    elif salto + 0 >= 2:
        PANTALLA.blit(salta[cuentaPasos // 1], (int(px), int(py)))
        cuentaPasos += 1

    else:
        PANTALLA.blit(quieto, (int(px), int(py)))


ejecuta = True

# Bucle de acciones y controles
while ejecuta:
    # FPS

    clock.tick(FPS)
    #esto es para que vaya bajando y no sobrepase el limite de la pantalla
    if py < H-100:
        py += 1

    # Bucle del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecuta = False

    # Opción tecla pulsada
    keys = pygame.key.get_pressed()

    # Tecla A - Movimiento a la izquierda
    if keys[pygame.K_a] and px > velocidad:
        px -= velocidad
        izquierda = True
        derecha = False

    # Tecla D - Movimiento a la derecha. La condicion para que no supere el ancho de la pantalla
    elif keys[pygame.K_d] and px < W - velocidad - ancho:
        px += velocidad
        izquierda = False
        derecha = True

    # Personaje quieto
    else:
        izquierda = False
        derecha = False
        cuentaPasos = 0

    # Tecla W - Movimiento hacia arriba
    if keys[pygame.K_w] and py > 100:
        py -= velocidad

    # Tecla S - Movimiento hacia abajo
    if keys[pygame.K_s] and py < 300:
        py += velocidad
    # Tecla SPACE - Salto
    if not salto:
        if keys[pygame.K_SPACE]:
            salto = True
            izquierda = False
            derecha = False
            cuentaPasos = 0
    else:
        if cuentaSalto >= -10:
            py -= (cuentaSalto * abs(cuentaSalto)) * 0.5
            cuentaSalto -= 1
        else:
            cuentaSalto = 10
            salto = False

    # Control del audio
    # Baja volumen con tecla 9
    if keys[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
        PANTALLA.blit(sonido_abajo, (850, 25))
    elif keys[pygame.K_9] and pygame.mixer.music.get_volume() == 0.0:
        PANTALLA.blit(sonido_mute, (850, 25))

    # Sube volumen con el numero 0
    if keys[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)
        PANTALLA.blit(sonido_arriba, (850, 25))
    elif keys[pygame.K_0] and pygame.mixer.music.get_volume() == 1.0:
        PANTALLA.blit(sonido_max, (850, 25))

    # Desactivar sonido con la tecla M
    elif keys[pygame.K_m]:
        pygame.mixer.music.set_volume(0.0)
        PANTALLA.blit(sonido_mute, (850, 25))

    # Reactivar sonido la tecla ,
    elif keys[pygame.K_COMMA]:
        pygame.mixer.music.set_volume(1.0)
        PANTALLA.blit(sonido_max, (850, 25))

    # Actualización de la ventana
    pygame.display.update()
    # Llamada a la función de actualización de la ventana
    recargaPantalla()

# Salida del juego
pygame.quit()

# bucle del joc
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#     # obtenim el ample del fons, perque retorni "el resto"
#     y_relativa = y % bg_img.get_rect().height
#     # li restem el valor de y relativa - el ample del fons (li posem a la y perque es mogui arriba abaix)
#     PANTALLA.blit(bg_img, (0, y_relativa - bg_img.get_rect().height))
#     if y_relativa < W:
#         PANTALLA.blit(bg_img, (0, y_relativa))
#
#     # aqui es posa x que es perque agafara la posicio que li digui la x, per aixo aniras cambiant la x o la y
#     y = y - 1
#     PANTALLA.blit(quieto, (int(px), int(py)))
#     pygame.display.update()
#
#     clock.tick(FPS)
