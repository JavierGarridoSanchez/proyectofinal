import pygame


class UI:
    def __init__(self, surface):
        self.current_health_ratio = None
        self.current_bar_width = None

        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('graphics/ui/health_bar.png')
        self.health_bar_topleft = (54, 39)
        # anchura barra salud
        self.bar_max_width = 152
        # que tan alta
        self.bar_height = 4

        # coins
        self.coin = pygame.image.load('graphics/ui/coin.png')
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))
        # le pasamos la fuente y el tamaño
        self.font = pygame.font.Font('graphics/ui/ARCADEPI.ttf', 30)

    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (20, 10))
        # indice de salud actual, sera nuestr salud actual / por salud completa
        # y de esta manera obtendriamos porcentajes en terminos de cuanta salud tenemos,
        # no un numero especifico, de esta manera no importaria que numero sea nuestra salud maxima,
        # porque siempre obtendremos un porcentaje, asi si quieremos cambiar la salud maxima, sera mas dinamico
        self.current_health_ratio = current / full
        self.current_bar_width = self.bar_max_width * self.current_health_ratio
        # ycon esto de arriba mult el max width por el porcentaje,
        # obtendremos un ancho de pixel especifico

        # ahora creamos un rectangulo de barra de salud, primero es para la posicion,
        # y la segunda tupla para el tamaño, x e y, es decir, tamaño x e y, primero altura, y luego anchura

        health_bar_rect = pygame.Rect(self.health_bar_topleft, (self.current_bar_width, self.bar_height))
        # lo pintamos con la pantala, color y el rectangulo que queremos pintar.
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, '#33323d')
        # obtenemos el rectangulo
        # sabemos donde esta el grafico de la moneda,
        # asi que quiero obtener el medio del lado dcerecho,
        # y luego ir unos pixeles a la derecha para colocar el texto ahi
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)
