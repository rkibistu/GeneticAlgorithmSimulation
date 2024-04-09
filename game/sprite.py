import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty, scalingFactor = 1):
        super().__init__()

        self.image = pygame.image.load(image)
        self.scaledImage = pygame.transform.scale(self.image, (int(self.image.get_width() * scalingFactor),
                                                           int(self.image.get_height() * scalingFactor)))

        self.rect = self.scaledImage.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.scaledImage, self.rect)

