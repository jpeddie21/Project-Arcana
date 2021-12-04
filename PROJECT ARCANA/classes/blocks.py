import pygame
import random
from classes import globals


class Block(pygame.sprite.Sprite):
    """ This class represents the general block class. """

    def __init__(self):
        """ Constructor, create the image of the block. """

        super().__init__()

        self.image = globals.enemy_sprite
        self.image.set_colorkey(globals.WHITE)
        self.image = pygame.transform.scale(self.image, (40, 50))
        self.rect = self.image.get_rect()
        self.shoot_num = random.randint(0, 4)
        self.speed_x = random.randrange(-2, 2)
        self.speed_y = random.randrange(1, 4)

    def reset_pos(self):
        """ Called when the block is 'collected' or falls off
            the screen. """

        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(40, 760)

    def update(self):
        """ Automatically called when we need to move the block. """

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y > globals.SCREEN_HEIGHT + self.rect.height:
            self.reset_pos()

        if self.rect.x > globals.SCREEN_WIDTH + self.rect.width or self.rect.x < 0 - self.rect.width:
            self.reset_pos()
