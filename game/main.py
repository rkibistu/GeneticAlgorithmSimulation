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
from plotUtils import plot_all
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

def mutate(org):
    newVelocity = org.v
    newSenseDist = org.d_food_max
    if(random.randrange(0,100) < 50):
        if(random.randrange(0,100) % 2 == 0):
            #mutate sense
            if(random.randrange(0,100) % 2 == 0):
                newSenseDist += 20
            else:
                newSenseDist -= 20
        else:
            #mutate speed
            if(random.randrange(0,100) % 2 == 0):
                newVelocity += 1
            else:
                newVelocity -= 1
    return Entity(settings.settings, wih=org.wih, who=org.who, name=org.name, velocity=newVelocity, sense=newSenseDist)

# no food -> die
# food, no home -> live
# enough food and home -> reproduce = dublicate + mutation
def evolve_v2(settings, organisms_old, gen):
    organisms_new = []
    stats = defaultdict(int)

    stats['V_MIN'] = 100
    stats['V_MAX'] = 0
    stats['V_AVG'] = 0
    stats['POP_NO'] = 0
    stats['SENSE_MIN'] = 1000
    stats['SENSE_MAX'] = 0
    stats['SENSE_AVG'] = 0

    organisms_alive = 0
    for org in organisms_old:
        if(org.fitness >= org.food_to_live):
            organisms_alive += 1

    # TODO: preserve the ones who just lived. preserve the elitism. And reproduce from elitism suing crossover, but creates onl 1 new organism

    # elitism (all that collected 2 food and arivved home)
    orgs_sorted = sorted(organisms_old, key=operator.attrgetter('finishedWork'), reverse=True)
    organisms_new = []
    elitism_number = 0
    elitism_organisms = []
    for org in orgs_sorted:
        if(org.finishedWork == 0):
            break
        elitism_number += 1
        elitism_organisms.append(Entity(settings, wih=org.wih, who=org.who, name=org.name, velocity=org.v, sense=org.d_food_max))

    crossover_number = int((organisms_alive - elitism_number)/2)
    for i in range(0,crossover_number):
        # select candidates
        canidates = range(0, elitism_number - 1)
        random_index = random.sample(canidates, 2)
        org_1 = elitism_organisms[random_index[0]]
        org_2 = elitism_organisms[random_index[1]]

        # crossover
        crossover_weight = random.random()
        velocity_new1 = (crossover_weight * org_1.v) + ((1 - crossover_weight) * org_2.v)
        velocity_new2 = (crossover_weight * org_2.v) + ((1 - crossover_weight) * org_1.v)
        
        org_1.v = velocity_new1
        org_2.v = velocity_new2
        newOrg1 = mutate(org_1)
        newOrg2 = mutate(org_2)

        organisms_new.append(newOrg1)
        organisms_new.append(newOrg2)
    organisms_new += elitism_organisms

    v_sum = 0
    sense_sum = 0
    print(organisms_new[0])
    for org in organisms_new:
        #STATS
        v_sum += org.v
        sense_sum += org.d_food_max
        if(org.v < stats['V_MIN']):
            stats['V_MIN'] = org.v
        if(org.v > stats['V_MAX']):
            stats['V_MAX'] = org.v
        if(org.d_food_max < stats['SENSE_MIN']):
            stats['SENSE_MIN'] = org.d_food_max
        if(org.d_food_max > stats['SENSE_MAX']):
            stats['SENSE_MAX'] = org.d_food_max

        org.reset()

    stats['POP_NO'] = len(organisms_new)
    stats['V_AVG'] = (v_sum)/stats['POP_NO']
    stats['SENSE_AVG'] = (sense_sum)/stats['POP_NO']
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

        for org in organisms:
             org.update(foods)   

        draw_game(settings,organisms,foods,gen,t_step, screen)

    return organisms


def concatenate_replace_and_split(num1, num2, x, replacement):
    # Convert numbers to binary strings
    binary1 = bin(num1)[2:]
    binary2 = bin(num2)[2:]

    # Concatenate binary strings
    concatenated = binary1 + binary2
    print(binary1)
    print(binary2)
    print(concatenated)

    # Replace first x bits with replacement
    modified = replacement + concatenated[x:]

    # Split modified bits into two parts
    split_index = len(binary1)
    modified_part1 = modified[:split_index]
    modified_part2 = modified[split_index:]

    print(modified_part1)
    print(modified_part2)

    # Convert modified binary strings back to integers
    new_num1 = int(modified_part1, 2)
    new_num2 = int(modified_part2, 2)

    return new_num1, new_num2

def main():

    # num1 = 5
    # num2 = 10
    # x = 4
    # replacement = '1100'  # Replace first x bits with this value

    # a,b = concatenate_replace_and_split(num1, num2, x, replacement)
    # print("a:", a, "  b:",b)
    # exit(1)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    print(Entity.__dir__)

    # dpawn organisms
    organisms = []
    for i in range(0,settings.settings['pop_size']):
        wih_init = np.random.uniform(-1, 1, (settings.settings['hnodes'], settings.settings['inodes']))     # mlp weights (input -> hidden)
        who_init = np.random.uniform(-1, 1, (settings.settings['onodes'], settings.settings['hnodes']))     # mlp weights (hidden -> output)

        wih_init = np.array(GOOD_WIH)
        who_init = np.array(GOOD_WHO)
        organisms.append(Entity(settings.settings, wih_init, who_init, name='gen[x]-org['+str(i)+']'))

    # generations loop
    food_quantity = settings.settings['food_num']
    for gen in range(0, settings.settings['gens']):

        # spawn food
        foods = []
        for i in range(0,food_quantity):
            foods.append(Food(settings.settings))
        food_quantity -= 1
        if(food_quantity < 10):
            food_quantity = 10

        organisms = simulate(settings.settings, organisms, foods, gen, screen)

        # organisms, stats = evolve(settings.settings, organisms, gen)
        organisms, stats = evolve_v2(settings.settings, organisms, gen)
        print('> GEN: ',gen,'POP_SIZE:',stats['POP_NO'],
              'V_MIN:',stats['V_MIN'], 'V_MAX:',stats['V_MAX'], 'V_AVG:',stats['V_AVG'],
              'SENSE_MIN:',stats['SENSE_MIN'], 'SENSE_MAX:',stats['SENSE_MAX'], 'SENSE_AVG:',stats['SENSE_AVG'])
        #print('> GEN:',gen,'BEST:',stats['BEST'],'AVG:',stats['AVG'],'WORST:',stats['WORST'])

        plot_all(gen,organisms,stats)

    while True:
        pass

if __name__ == "__main__":
    main()