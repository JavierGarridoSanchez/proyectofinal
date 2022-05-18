import pygame

class UI:
    def __init__(self, surface):
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('graphics/ui/healyh_bar.png')
