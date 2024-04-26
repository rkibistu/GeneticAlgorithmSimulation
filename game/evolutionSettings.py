settings = {}

# EVOLUTION SETTINGS
settings['pop_size'] = 100      # number of organisms
settings['food_num'] = 50       # number of food particles
settings['gens'] = 50           # number of generations
settings['elitism'] = 0.20      # elitism (selection bias)
settings['mutate'] = 0.10       # mutation rate

# SIMULATION SETTINGS
settings['gen_time'] = 100      # generation length         (seconds)
settings['dt'] = 0.04           # simulation time step      (dt)
settings['dr_max'] = 720        # max rotational speed      (degrees per second)
settings['v_max'] = 8.0         # max velocity              (units per second)
settings['v_min'] = 7.99        # min velocity              (units per second)
settings['v_max_color'] = 20.0  # the max value used to get the color based on velcoity
settings['v_min_color'] = 4.0  # the min value used to get the color based on velcoity
settings['dv_max'] =  2         # max acceleration (+/-)    (units per second^2)

settings['x_min'] = 10.0        # arena western border
settings['x_max'] =  1250.0     # arena eastern border
settings['y_min'] = 5.0         # arena southern border
settings['y_max'] =  710.0      # arena northern border

settings['plot'] = True         # plot final generation?

# ORGANISM NEURAL NET SETTINGS
settings['inodes'] = 1          # number of input nodes
settings['hnodes'] = 5          # number of hidden nodes
settings['onodes'] = 2          # number of output nodes

