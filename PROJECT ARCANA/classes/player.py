import pygame
from classes import globals


class Player(pygame.sprite.Sprite):
    """ This class represents the player. """

    def __init__(self, x, y):
        """ Constructor, creates image of the player. """

        super().__init__()

        self.image = globals.player_sprite
        self.image.set_colorkey(globals.WHITE)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0

    def change_speed(self, x, y):
        """ Change the speed of the player"""

        self.change_x += x
        self.change_y += y

    def update(self):
        """ Find a new position for the player"""

        if (self.rect.x >= -4) & (self.rect.x <= 800):
            if self.rect.x < 0:
                self.rect.x = 0
            if self.rect.x > 740:
                self.rect.x = 740
            self.rect.x += self.change_x
        if (self.rect.y >= 40) and (self.rect.y <= 900):
            if self.rect.y < 45:
                self.rect.y = 45
            if self.rect.y > 840:
                self.rect.y = 840
        self.rect.y += self.change_y
