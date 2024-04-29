settings = {}

# EVOLUTION SETTINGS
settings['pop_size'] = 100      # number of organisms
settings['food_num'] = 50       # number of food particles
settings['gens'] = 500           # number of generations
settings['elitism'] = 0.20      # elitism (selection bias)
settings['mutate'] = 0.10       # mutation rate

# SIMULATION SETTINGS
settings['gen_time'] = 100          # generation length         (seconds)
settings['dt'] = 0.04               # simulation time step      (dt)
settings['dr_max'] = 720            # max rotational speed      (degrees per second)
settings['v_max'] = 8.01            # max velocity at spawn             (units per second)
settings['v_min'] = 8.00            # min velocity at spawn             (units per second)
settings['v_max_alltime'] = 50.0      # range used to map velocity to color
settings['v_min_alltime'] = 1.0       
settings['dv_max'] =  2             # max acceleration (+/-)    (units per second^2)
settings['sense_min'] = 50          # min value of distance to see food around
settings['sense_max'] = 50.01       # max value of distance to see food around
settings['sense_min_color'] = 30    # range used to map sense to color
settings['sense_max_color'] = 120

settings['x_min'] = 10.0        # arena western border
settings['x_max'] =  1250.0     # arena eastern border
settings['y_min'] = 5.0         # arena southern border
settings['y_max'] =  710.0      # arena northern border

settings['plot'] = True         # plot final generation?

# ORGANISM NEURAL NET SETTINGS
settings['inodes'] = 1          # number of input nodes
settings['hnodes'] = 5          # number of hidden nodes
settings['onodes'] = 2          # number of output nodes

