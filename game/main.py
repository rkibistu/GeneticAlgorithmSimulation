import pygame
import random
from math import atan2
from math import cos
from math import degrees
from math import floor
from math import radians
from math import sin
from math import sqrt
from collections import defaultdict
import numpy as np
import operator
import sys


from entity import Entity
from food import Food
import evolutionSettings as settings

WIDTH = 1280
HEIGHT = 720
BACKGROUND = (0, 0, 0)

# some good values saved
GOOD_WIH = [
    -0.51089986,
    -0.26583297,
    -0.97804446,
    -0.10858291,
    -0.69969082,
]
GOOD_WHO = [
    [0.66994817, -0.55868148, 0.24482176, 0.4597497, 0.31503457],
    [0.16009314, -0.08497293, -0.60829999, -0.69862888, -0.13360536]
]

def dist(x1,y1,x2,y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def calc_heading(org, food):
    d_x = food.x - org.x
    d_y = food.y - org.y
    theta_d = degrees(atan2(d_y, d_x)) - org.r
    if abs(theta_d) > 180: theta_d += 360
    return theta_d / 180

def draw_game(settings, organisms, foods, gen, time, screen):

    screen.fill(BACKGROUND)

    for organism in organisms:
        organism.draw(screen)
    for food in foods:
        food.draw(screen)
    
    pygame.display.flip()

def evolve(settings, organisms_old, gen):

    elitism_num = int(floor(settings['elitism'] * settings['pop_size']))
    new_orgs = settings['pop_size'] - elitism_num

    # Get current generation stats
    stats = defaultdict(int)
    for org in organisms_old:
        if org.fitness > stats['BEST'] or stats['BEST'] == 0:
            stats['BEST'] = org.fitness
            stats['BEST-WIH'] = org.wih
            stats['BEST-WHO'] = org.who

        if org.fitness < stats['WORST'] or stats['WORST'] == 0:
            stats['WORST'] = org.fitness

        stats['SUM'] += org.fitness
        stats['COUNT'] += 1

    stats['AVG'] = stats['SUM'] / stats['COUNT']


    # elitism
    orgs_sorted = sorted(organisms_old, key=operator.attrgetter('fitness'), reverse=True)
    organisms_new = []
    for i in range(0, elitism_num):
        organisms_new.append(Entity(settings, wih=orgs_sorted[i].wih, who=orgs_sorted[i].who, name=orgs_sorted[i].name))


    # Generate new organisms
    for w in range(0, new_orgs):

        # select candidates
        canidates = range(0, elitism_num)
        random_index = random.sample(canidates, 2)
        org_1 = orgs_sorted[random_index[0]]
        org_2 = orgs_sorted[random_index[1]]

        # crossover
        crossover_weight = random.random()
        wih_new = (crossover_weight * org_1.wih) + ((1 - crossover_weight) * org_2.wih)
        who_new = (crossover_weight * org_1.who) + ((1 - crossover_weight) * org_2.who)

        # Mutate
        mutate = random.random()
        if mutate <= settings['mutate']:

            mat_pick = random.randint(0,1)

            # mutate WIH weights
            if mat_pick == 0:
                index_row = random.randint(0,settings['hnodes']-1)
                wih_new[index_row] = wih_new[index_row] * random.uniform(0.9, 1.1)
                if wih_new[index_row] >  1: wih_new[index_row] = 1
                if wih_new[index_row] < -1: wih_new[index_row] = -1

            # mutate WHO weights
            if mat_pick == 1:
                index_row = random.randint(0,settings['onodes']-1)
                index_col = random.randint(0,settings['hnodes']-1)
                who_new[index_row][index_col] = who_new[index_row][index_col] * random.uniform(0.9, 1.1)
                if who_new[index_row][index_col] >  1: who_new[index_row][index_col] = 1
                if who_new[index_row][index_col] < -1: who_new[index_row][index_col] = -1

        organisms_new.append(Entity(settings, wih=wih_new, who=who_new, name='gen['+str(gen)+']-org['+str(w)+']'))

    return organisms_new, stats

def handle_events():
  for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def simulate(settings, organisms, foods, gen, screen):

    total_time_steps = int(settings['gen_time'] / settings['dt'])

    # simulation loop
    for t_step in range(0, total_time_steps, 1):

        handle_events()

        draw_game(settings,organisms,foods,gen,t_step, screen)

        # update fitness function
        for food in foods:
            for org in organisms:
                food_org_dist = dist(org.x, org.y, food.x, food.y)

                # if organism is close enough to the food -> eat it
                if food_org_dist <= 0.75:
                    org.fitness += food.energy
                    food.respawn(settings)

                # reset values so they will be calcualted again
                org.d_food = 100
                org.r_food = 0

        # calcilate heading to closest food
        for food in foods:
            for org in organisms:

                food_org_dist = dist(org.x, org.y, food.x, food.y)
                if food_org_dist < org.d_food:
                    org.d_food = food_org_dist
                    org.r_food = calc_heading(org, food)

        # update internal values using neuronal network
        for org in organisms:
            org.think()

        # update position and velocity
        for org in organisms:
            org.update_r(settings)
            org.update_vel(settings)
            org.update_pos(settings)

    return organisms

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    print(Entity.__dir__)

    # spawn food
    foods = []
    for i in range(0,settings.settings['food_num']):
        foods.append(Food(settings.settings))

    # dpawn organisms
    organisms = []
    for i in range(0,settings.settings['pop_size']):
        wih_init = np.random.uniform(-1, 1, (settings.settings['hnodes'], settings.settings['inodes']))     # mlp weights (input -> hidden)
        who_init = np.random.uniform(-1, 1, (settings.settings['onodes'], settings.settings['hnodes']))     # mlp weights (hidden -> output)

        wih_init = np.array(GOOD_WIH)
        who_init = np.array(GOOD_WHO)
        organisms.append(Entity(settings.settings, wih_init, who_init, name='gen[x]-org['+str(i)+']'))

    # generations loop
    for gen in range(0, settings.settings['gens']):

        organisms = simulate(settings.settings, organisms, foods, gen, screen)

        organisms, stats = evolve(settings.settings, organisms, gen)
        print('> GEN:',gen,'BEST:',stats['BEST'],'AVG:',stats['AVG'],'WORST:',stats['WORST'])
        print('> WIH: ', stats['BEST-WIH'])
        print('> WHO: ', stats['BEST-WHO'])

if __name__ == "__main__":
    main()