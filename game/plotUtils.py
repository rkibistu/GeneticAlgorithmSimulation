import matplotlib.pyplot as plt

# PLOT VARIABLES
plt.ion()
velocity_avg_fig = plt.figure(num="avg velocity")
population_count_fig = plt.figure(num="population count")
individual_velocity_fig = plt.figure(num="individual velocity")
velocity_avg_ax = velocity_avg_fig.add_subplot(111)
population_count_ax = population_count_fig.add_subplot(111)
individual_velocity_ax = individual_velocity_fig.add_subplot(111)

g_v_avg = []    # avg velocity of every generation
g_pop_no = []   # pop count of ef very generation
g_x_plot = []


def plot_stats(gen, stats):
    g_v_avg.append(stats['V_AVG'])
    g_pop_no.append(stats['POP_NO'])
    g_x_plot.append(gen)

    if(gen < 2):
        return

    line1, = velocity_avg_ax.plot(g_x_plot, g_v_avg)
    velocity_avg_fig.canvas.draw()
    velocity_avg_fig.canvas.flush_events()

    line1, = population_count_ax.plot(g_x_plot,g_pop_no)
    population_count_fig.canvas.draw()
    population_count_fig.canvas.flush_events()

def plot_current_generation(gen, organisms):
    org_velocity = []

    for org in organisms:
        org_velocity.append(org.v)

    individual_velocity_ax.hist(org_velocity, bins=20, color='skyblue', edgecolor='black')
    individual_velocity_fig.canvas.draw()
    individual_velocity_fig.canvas.flush_events()

def plot_all(gen, organisms, stats):
    plot_stats(gen,stats)
    plot_current_generation(gen,organisms)
    plt.cla()
