from sprite import Sprite
import random
import numpy as np
import pygame
import math

from food import Food
import evolutionSettings as settings

class Entity(pygame.sprite.Sprite):
    def __init__(self, settings, wih=None, who=None, name=None, velocity=None):
        super().__init__()

        self.image = pygame.image.load("Sprites/triangle.png")
        scalingFactor = 0.05
        self.scaledImage = pygame.transform.scale(self.image, (int(self.image.get_width() * scalingFactor),
                                                           int(self.image.get_height() * scalingFactor)))
        self.rect = self.scaledImage.get_rect()

        self.x,self.y = generate_pos_on_box_margins(
            settings["x_min"], 
            settings["y_min"], 
            settings["x_max"], 
            settings["y_max"]
            )
        self.origin_x = self.x
        self.origin_y = self.y

        self.rect.center = [self.x, self.y]

        self.r = random.uniform(0,360)                 # orientation   [0, 360]
        if(velocity == None):
            self.v = random.uniform(settings['v_min'],settings['v_max'])   # velocity      [0, v_max]
        else:
            self.v = velocity
        self.dv = random.uniform(-settings['dv_max'], settings['dv_max'])   # dv

        self.d_food_max = 100 # max distance it can detects food
        self.d_food = 100   # distance to nearest food
        self.r_food = 0     # orientation to nearest food
        self.fitness = 0    # fitness (food count)

        self.food_to_reproduce = 2  # food count to reproduce
        self.food_to_live = 1       # food count to live
        self.finishedWork = 0

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

    def update(self, foods):
        self.calc_heading(foods)
        self.think()
        self.update_r(settings.settings)
        self.update_pos(settings.settings)
        self.try_eat(foods)
        self.try_mark_back_home()

    def reset(self):
        self.x,self.y = generate_pos_on_box_margins(
            settings.settings["x_min"], 
            settings.settings["y_min"], 
            settings.settings["x_max"], 
            settings.settings["y_max"]
            )
        self.origin_x = self.x
        self.origin_y = self.y

        self.rect.center = [self.x, self.y]

        self.d_food = 100   # distance to nearest food
        self.r_food = 0     # orientation to nearest food
        self.fitness = 0

        self.finishedWork = 0

       

    def set_color(self, surface, color):
        rect = surface.get_rect()
        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        surf.fill(color)
        return surf

    # draw
    def draw(self, screen):
        
        a = self.set_color(self.scaledImage,velocity_to_rgb(self.v,settings.settings['v_min'], settings.settings['v_max']))
        a = self.set_color(self.scaledImage,velocity_to_rgb(self.v,5, 20))
        screen.blit(a, self.rect)

    # iterates foods array and eat the one close enough
    def try_eat(self, foods):
        eaten_foods = []
        for food in foods:
                food_org_dist = dist(self.x, self.y, food.x, food.y)

                # if organism is close enough to the food -> eat it
                if food_org_dist <= 0.90:
                    self.fitness += food.energy
                    #food.respawn(settings.settings)
                    eaten_foods.append(food)

                # reset values so they will be calcualted again
                self.d_food = 100
                self.r_food = 0

        # remove all eaten food from the foods array
        for eaten_food in eaten_foods:
            foods.remove(eaten_food)

    # mark back home flag if entity is home and have enough food
    def try_mark_back_home(self):
        home_org_dist = dist(self.x, self.y, self.origin_x, self.origin_y)
        if home_org_dist <= 0.90 and self.fitness >= self.food_to_reproduce:
            self.finishedWork = 1

    
    # calc rotation to closest food
    def calc_heading(self,foods):
        #try to find food
        for food in foods:
            food_org_dist = dist(self.x, self.y, food.x, food.y)
            if food_org_dist < self.d_food:
                self.d_food = food_org_dist
                self.r_food = heading(self, food.x, food.y)

        #if no food detected and touch margins, orient to center of the screen
        if (self.d_food == self.d_food_max and 
            not is_inside_box(self,settings.settings['x_min'],settings.settings['y_min'],settings.settings['x_max'],settings.settings['y_max'])) :
            
            self.r_food = heading(self, settings.settings['x_max']/2, settings.settings['y_max']/2 )

        #if you collected enough food -> go home
        if(self.fitness >= self.food_to_reproduce):
            self.r_food = heading(self, self.origin_x, self.origin_y)

    # UTILS
def dist(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def heading(pos, target_x, target_y):
    d_x = target_x - pos.x
    d_y = target_y - pos.y
    theta_d = math.degrees(math.atan2(d_y, d_x)) - pos.r
    if abs(theta_d) > 180: theta_d += 360
    return theta_d / 180

def generate_pos_on_box_margins(x1,y1,x2,y2):
    x = 0
    y = 0
    if(random.randrange(0,10) % 2 ==0):
        x = random.uniform(x1, x2)  # position (x)
        #random up or both
        if(random.randrange(0,10) % 2 ==0):
                y = y1
        else:
                y = y2
    else:
        y = random.uniform(y1, y2)  # position (y)
        #random left or right
        if(random.randrange(0,10) % 2 ==0):
            x = x1
        else:
            x = x2

    return x,y

def is_inside_box(pos, x1,y1,x2,y2):
    min_x = min(x1,x2)
    min_y = min(y1,y2)
    max_x = max(x1,x2)
    max_y = max(y1,y2)

    if min_x <= pos.x <= max_x and min_y <= pos.y <= max_y:
        return True
    return False

def velocity_to_rgb(velocity, min_velocity, max_velocity):
    # Normalize velocity to range [0, 1]
    normalized_velocity = (velocity - min_velocity) / (max_velocity - min_velocity)
    print(normalized_velocity)
    # Map normalized velocity to RGB color space
    red = int(255 * normalized_velocity)
    green = 0
    blue = int(255 * (1 - normalized_velocity))
    
    return [red, green, blue]