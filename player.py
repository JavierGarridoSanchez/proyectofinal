import pygame

from support import import_folder
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, change_health):
        self.import_char()
        super().__init__()
        self.frame_index = 0
        self.name = None


        # sonido salto
        self.jump_sound = pygame.mixer.Sound('audio/effects/jump.wav')
        self.hit_sound = pygame.mixer.Sound('audio/effects/hit.wav')

        # particulas
        self.import_dust_part()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface

        # velocidad de animacion de frames
        self.animation_speed = 0.15
        # elijo la animacion idle que es la quieta por defecto.
        self.image = self.animations['idle'][self.frame_index].convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        # movimiento del player
        # la dirección es un vector el cual solo indica en que dirección
        # se está moviendo no le estamos diciendo que se printe la cantidad "direccion"
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -25
        # creamos un nuevo triangulo para abordar solo la parte del rect sin la espada
        # con el top left le especificas la parte de arriba izquierda del rect, y con el size,
        # el tamaño de la colision que pillaras del rectandulo,
        # es decir pillaras un rectangulo mas pequeño del rectangulo
        self.collision_rect = pygame.Rect(self.rect.topleft, (20, self.rect.height))

        # estado del jugador
        self.status = 'idle'
        self.looking_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # health
        self.change_health = change_health
        # esto se hara porque necesitas ponerlo invencible al perso, y darle un tiempo,
        # ya que sino, el numero de fotogramas haria que la vida bajase toda de golpe
        # ya que va a 60 fotogramas
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0

        # hay un fallo de colision, y es cuando saltas
        # y sueltas en el aire el salto y le das a la derecha,
        # siempre cuando estas pegado un muro

    def import_char(self):
        char_path = 'graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = char_path + animation
            self.animations[animation] = import_folder(full_path)

    # esto es para saber si el jugador esta en x direccion para hacer el
    # cambio de sprite correspondiente

    def player_name(self, name):
        self.name = name
        return self.name

    def get_damage(self):
        # esto lo hacemos porque si en cada fotograma le quita 10 health,
        # la vida bajaria de golpe, por lo que se le da una invencibilidad y un tiempo

        if not self.invincible:
            self.hit_sound.play()
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            # si el tiempo actual - el tiempo de daño,
            # es mayor o igual al de la duracion de invicibilidad entonces
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    # sinosuidal, que ira alternando entre 1 y -1 para hacer al perosnaje invisible,
    # es como una onda
    # lo que haremos es si esta por encima de 0,
    # devolvere 255 (transparencia total, osea visible),
    # así estamos por debajo de 0 sin transparencia, osea invisibles
    def wave_value(self):
        # valor x es el tiempo
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def import_dust_part(self):
        self.dust_run_part = import_folder('graphics/character/dust_particles/run')

    def run_dust_animation(self):
        # si esta en run y en el suelo
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_part):
                self.dust_frame_index = 0
            dust_particle = self.dust_run_part[int(self.dust_frame_index)]
            # y esto es para mirar si el personaje esta a la izq o derecha,
            # para que las particulas de polvo apunten a una dire tb
            if self.looking_right:
                # si el personaje se mueve a la derecha el polvo aparecera en la izq
                # si no fuera con vector,
                # tendria que apuntar directamente abajo a la izquierda pos
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)

            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'

        # si el personaje tiene un movimiento diferente de 0,
        # sabemos que esta corriendo ya que no sera 0
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    # 1:47
    def animate(self):
        # obtenemos las imagenes de run
        animation = self.animations[self.status]

        # loop frames indice
        self.frame_index += self.animation_speed
        # con esto es para que no supere el indice del numero de imagenes,
        # hara un loop infinito volviendo a la animacion 0
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.looking_right:
            self.image = image
            # cambiamos la colision al left para que si miras a la derecha,
            # la parte de la espada no colision en la izquierda
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            # si no miramos hacia la derecha, entonces volteamos la imagen
            imagen_invertida = pygame.transform.flip(image, True, False)
            self.image = imagen_invertida
            self.rect.bottomright = self.collision_rect.bottomright

        # obtengo valores alpha para hacer que el personaje desaparezca y no,
        # osea parpadee cuando le pegan
        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)

        else:
            # devolvemos la transparencia
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        # rect
        # si el jugador esta tocando el suelo y a la derecha,
        # la posicion sera donde estaba el rectangulo
        # if self.on_ground and self.on_right:
        #     self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        # elif self.on_ground and self.on_left:
        #     self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        # elif self.on_ground:
        #     self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        #
        # elif self.on_ceiling and self.on_right:
        #     self.rect = self.image.get_rect(topright=self.rect.topright)
        # elif self.on_ceiling and self.on_left:
        #     self.rect = self.image.get_rect(topleft=self.rect.topleft)
        # elif self.on_ceiling:
        #     self.rect = self.image.get_rect(midtop=self.rect.midtop)

        # el punto medio de la parte superior,
        # sera la mitad de la parte superior del rectangulo anterior

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.looking_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.looking_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):

        self.direction.y = self.jump_speed
        # colocar un if statement para controlar el sonido
        self.jump_sound.stop()
        self.jump_sound.play()

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()
        self.wave_value()
