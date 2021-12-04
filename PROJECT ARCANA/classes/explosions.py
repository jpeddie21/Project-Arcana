import pygame


class Explosion(pygame.sprite.Sprite):
    """ This class represents the explosions. """

    def __init__(self, x, y):
        super().__init__()

        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"images/exp{num}.png")
            img = pygame.transform.scale(img, (60, 60))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):

        explosion_speed = 3
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
