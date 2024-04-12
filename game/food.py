
import pygame
import random


class Food(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()

        self.image = pygame.image.load("Sprites/circle.png")
        scalingFactor = 0.05
        self.scaledImage = pygame.transform.scale(self.image, (int(self.image.get_width() * scalingFactor),
                                                           int(self.image.get_height() * scalingFactor)))
        self.rect = self.scaledImage.get_rect()

        self.x = random.uniform(settings['x_min'], settings['x_max'])
        self.y = random.uniform(settings['y_min'], settings['y_max'])
        self.rect.center = [self.x, self.y]
        self.energy = 1

    def respawn(self,settings):
        self.x = random.uniform(settings['x_min'], settings['x_max'])
        self.y = random.uniform(settings['y_min'], settings['y_max'])
        self.rect.center = [self.x, self.y]
        self.energy = 1

    # Draw
    def draw(self, screen):
        screen.blit(self.scaledImage, self.rect)