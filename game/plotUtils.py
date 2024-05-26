import matplotlib.pyplot as plt
import os
import shutil


save_folder = 'D:/Master/ALJV/saves/'
save = False
relative_path = ''

avg_vel_filename = 'avg_vel.png'
avg_sense_filename = 'avg_sense.png'
pop_count_filename = 'pop_count.png'
individual_vel_folder = 'individ_vel/'
individual_sense_folder = 'individ_sense/'

settings_file = 'D:/Master/ALJV/evolving-simple-organisms/game/evolutionSettings.py'

def ActivateSaving(foldername, force_recreate=False):
    global relative_path
    global save
    save = True
    relative_path = foldername + '/'
    if(force_recreate):
        shutil.rmtree(save_folder+relative_path)
    os.makedirs(save_folder+relative_path)
    os.makedirs(save_folder+relative_path+individual_vel_folder)
    os.makedirs(save_folder+relative_path+individual_sense_folder)
    shutil.copy(settings_file, save_folder+relative_path+'evolutionSettings.py')
    print("Activate saving to: ", save_folder + relative_path)

# PLOT VARIABLES
plt.ion()
velocity_avg_fig = plt.figure(num="avg velocity")
sense_avg_fig = plt.figure(num="avg sense")
population_count_fig = plt.figure(num="population count")
individual_velocity_fig = plt.figure(num="individual velocity")
individual_sense_fig = plt.figure(num="individual sense")
velocity_avg_ax = velocity_avg_fig.add_subplot(111)
sense_avg_ax = sense_avg_fig.add_subplot(111)
population_count_ax = population_count_fig.add_subplot(111)
individual_velocity_ax = individual_velocity_fig.add_subplot(111)
individual_sense_ax = individual_sense_fig.add_subplot(111)

g_v_avg = []            # avg velocity of every generation
g_sense_avg = []        # avg sense of every generation
g_pop_no = []           # pop count of ef very generation
g_x_plot = []


def plot_stats(gen, stats):
    g_v_avg.append(stats['V_AVG'])
    g_sense_avg.append(stats['SENSE_AVG'])
    g_pop_no.append(stats['POP_NO'])
    g_x_plot.append(gen)

    if(gen < 2):
        return

    line1, = velocity_avg_ax.plot(g_x_plot, g_v_avg)
    velocity_avg_fig.canvas.draw()
    velocity_avg_fig.canvas.flush_events()
    if(save):
        velocity_avg_fig.savefig(save_folder + relative_path + avg_vel_filename)

    line1, = sense_avg_ax.plot(g_x_plot, g_sense_avg)
    sense_avg_fig.canvas.draw()
    sense_avg_fig.canvas.flush_events()
    if(save):
        sense_avg_fig.savefig(save_folder + relative_path + avg_sense_filename)

    line1, = population_count_ax.plot(g_x_plot,g_pop_no)
    population_count_fig.canvas.draw()
    population_count_fig.canvas.flush_events()
    if(save):
        population_count_fig.savefig(save_folder + relative_path + pop_count_filename)

def plot_current_generation(gen, organisms):
    org_velocity = []
    org_sense = []

    for org in organisms:
        org_velocity.append(org.v)
        org_sense.append(org.d_food_max)

    individual_velocity_ax.cla()
    individual_velocity_ax.hist(org_velocity, bins=20, color='skyblue', edgecolor='black')
    individual_velocity_fig.canvas.draw()
    individual_velocity_fig.canvas.flush_events()
    individual_velocity_fig.savefig(save_folder+relative_path+individual_vel_folder+str(gen)+'.png')

    individual_sense_ax.hist(org_sense, bins=20, color='skyblue', edgecolor='black')
    individual_sense_fig.canvas.draw()
    individual_sense_fig.canvas.flush_events()
    individual_sense_fig.savefig(save_folder+relative_path+individual_sense_folder+str(gen)+'.png')

def plot_all(gen, organisms, stats):
    plt.cla()
    plot_stats(gen,stats)
    plot_current_generation(gen,organisms)
