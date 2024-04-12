from sprite import Sprite
import random
import math
import numpy as np
import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, settings, wih=None, who=None, name=None):
        super().__init__()

        self.image = pygame.image.load("Sprites/triangle.png")
        scalingFactor = 0.05
        self.scaledImage = pygame.transform.scale(self.image, (int(self.image.get_width() * scalingFactor),
                                                           int(self.image.get_height() * scalingFactor)))
        self.rect = self.scaledImage.get_rect()

        self.x = random.uniform(settings['x_min'], settings['x_max'])  # position (x)
        self.y = random.uniform(settings['y_min'], settings['y_max'])  # position (y)
        self.rect.center = [self.x, self.y]

        self.r = random.uniform(0,360)                 # orientation   [0, 360]
        self.v = random.uniform(0,settings['v_max'])   # velocity      [0, v_max]
        self.dv = random.uniform(-settings['dv_max'], settings['dv_max'])   # dv

        self.d_food = 100   # distance to nearest food
        self.r_food = 0     # orientation to nearest food
        self.fitness = 0    # fitness (food count)

        self.wih = wih
        self.who = who

        self.name = name

    # retea neuronala simpla
    def think(self):

        # mlp
        af = lambda x: np.tanh(x)               # activation function
        h1 = af(np.dot(self.wih, self.r_food))  # hidden layer
        out = af(np.dot(self.who, h1))          # output layer

        # update based on mlp response
        self.nn_dv = float(out[0])   # [-1, 1]  (accelerate=1, deaccelerate=-1)
        self.nn_dr = float(out[1])   # [-1, 1]  (left=1, right=-1)


    # update heading (rotation)
    def update_r(self, settings):
        self.r += self.nn_dr * settings['dr_max'] * settings['dt']
        self.r = self.r % 360


    # update velocity
    def update_vel(self, settings):
        self.v += self.nn_dv * settings['dv_max'] * settings['dt']
        if self.v < 0: self.v = 0
        if self.v > settings['v_max']: self.v = settings['v_max']


    # update position
    def update_pos(self, settings):
        dx = self.v * math.cos(math.radians(self.r)) * settings['dt']
        dy = self.v * math.sin(math.radians(self.r)) * settings['dt']
        self.x += dx
        self.y += dy
        self.rect.center = [self.x, self.y]

    # draw
    def draw(self, screen):
        screen.blit(self.scaledImage, self.rect)