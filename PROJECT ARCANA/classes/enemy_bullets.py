import pygame
from classes import globals


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        """ Constructor, creates image of the bullet. """

        super().__init__()

        self.image = globals.enemy_spell
        self.image.set_colorkey(globals.WHITE)
        self.image = pygame.transform.scale(self.image, (20, 40))
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """

        self.rect.y += 4

        if self.rect.y > 905:
            self.kill()
