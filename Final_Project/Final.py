import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time


start_time = time.time()
# -=MAIN CODE=-

class human(object):
    def __init__(self, coords=None, masking_rate=None):
        self.pos = np.array(coords)
        self.lerp_pos = self.pos
        self.start_angle = np.random.rand() * 2 * np.pi
        self.vel = np.array([np.cos(self.start_angle), np.sin(self.start_angle)])    # random direction, always speed of one
        self.radius = 0.5
        self.infected = False    # use infect to make the initial infected population
        self.infected_timer = virus_duration
        self.immune = False
        self.alive = True
        if masking_rate != None and masking_rate >= np.random.rand():
            self.mask = True
        else:
            self.mask = False
        assert coords is not None, "must pass coordinates to instantiate human object"

    def infect(self):
        self.infected = True

    def succumb(self):
        self.alive = False
        self.infected = False

    def wall_collide(self): # this isn't a great algorithm, but it is simple
        if (self.pos[0] - self.radius <= 0 and self.vel[0] <= 0) or (self.pos[0] + self.radius >= stage_width and self.vel[0] >= 0):
            self.vel[0] = self.vel[0] * -1
        if (self.pos[1] - self.radius <= 0 and self.vel[1] <= 0) or (self.pos[1] + self.radius >= stage_height and self.vel[1] >= 0):
            self.vel[1] = self.vel[1] * -1

    def interact(self, human2):
        # turns around at least 90 degrees
        new_traj_angle = np.random.rand()*np.pi + np.pi/2 
        rotation_matrix = np.array([[np.cos(new_traj_angle), -np.sin(new_traj_angle)], [np.sin(new_traj_angle), np.cos(new_traj_angle)]])
        self.vel = np.matmul(rotation_matrix, self.vel) # no change in speed

        # chance of infection (receiving, NOT sending)
        if human2.infected and not (self.infected or self.immune):
            if human2.mask and self.mask:
                if spread_two_mask >= np.random.rand():
                    self.infected = True
            elif human2.mask or self.mask:
                if spread_one_mask >= np.random.rand():
                    self.infected = True
            elif spread_no_mask >= np.random.rand():
                self.infected = True

    def infected_advance(self):
        # timer
        if self.infected:
            self.infected_timer -= deltat
        if self.infected_timer <= 0:
            self.infected = False
            self.immune = True

        # chance of death
        if death_chance >= np.random.rand() and self.infected:
            self.succumb()

    def advance(self):
        self.pos = self.pos + self.vel * deltat
        self.lerp_pos = self.pos
        self.wall_collide()
        self.infected_advance()

    def lerp_advance(self):
        self.lerp_pos = self.lerp_pos + self.vel * deltat / lerp_count



# -=PARAMETERS=-

# stage
stage_width = 55
stage_height = 55
human_spacing = 5
initial_infections = 1
lifetimes_simulated = 4

deltat = 0.5 # arbitrary time steps between calculations (not lerps)
lerp_count = 2 # frames of linear interpolation (number of interpolated frames PLUS ONE FOR THE CALCULATED FRAME!)

chance_of_mask = 0.40

# alien supervirus
spread_no_mask = 0.99
spread_one_mask = 0.33
spread_two_mask = 0.099 # masks are very effective
fatality_rate = 0.90
virus_duration = 100

death_chance = 1 - (1 - (fatality_rate))**(deltat/virus_duration) # chance per deltat of death

# manufacture the humans in the box
stage_humans = []
for i in range(human_spacing, stage_width, human_spacing):
    for j in range(human_spacing, stage_height, human_spacing):
        stage_humans.append(human(coords=[i,j], masking_rate=chance_of_mask))
for i in range(initial_infections):
    random.choice(stage_humans).infect()



# -=METRICS=-

timeline = np.arange(0, lifetimes_simulated*virus_duration, deltat)
healthy_count = np.zeros_like(timeline)
masked_healthy_count = np.zeros_like(timeline)
infected_count = np.zeros_like(timeline)
dead_count = np.zeros_like(timeline)
immune_count = np.zeros_like(timeline)



# -=ANIMATING=-

fig, ax = plt.subplots()
ax.set(xlim=[0, stage_width], ylim=[0,stage_height], xlabel='x', ylabel='y')

# making handles
handles = []
for person in stage_humans:
    if person.mask:
        handle = ax.scatter(person.pos[0], person.pos[1], marker='p')
    else:
        handle = ax.scatter(person.pos[0], person.pos[1])
    handles.append(handle)

def update(frame):
    ax.set_title(f"t = {np.round((frame * deltat / lerp_count), 2):.2f}")

    if frame % lerp_count == 0:
        for i, person in enumerate(stage_humans):

            # marker styles
            if person.infected:
                handles[i].set_color('red')
            elif person.immune:
                handles[i].set_color('#11cc11')
            elif not person.alive:
                handles[i].set_color('black')
            else:
                handles[i].set_color('blue')


            if person.alive:
                person.advance()
                for person2 in stage_humans[i+1:]:
                    if np.linalg.norm(person.pos - person2.pos) <= 2*person.radius and person.alive and person2.alive:
                        person.interact(person2)
                        person2.interact(person)
                handles[i].set_offsets([person.pos[0], person.pos[1]])

            if person.infected:
                infected_count[int(frame/lerp_count)] += 1
            elif person.immune:
                immune_count[int(frame/lerp_count)] += 1
            elif person.alive:
                healthy_count[int(frame/lerp_count)] += 1
            else:
                dead_count[int(frame/lerp_count)] += 1
            if person.alive and person.mask and not person.infected:
                masked_healthy_count[int(frame/lerp_count)] += 1
        
        if infected_count[int(frame/lerp_count)] == 0:
            print("There are no more infected people.  Break the simulation.  Choose the red pill, Neo.")
    else:  # linear interpolation for more frames!
        for i, person in enumerate(stage_humans):
            if person.alive:
                person.lerp_advance()
            handles[i].set_offsets([person.lerp_pos[0], person.lerp_pos[1]])



# final animation
ani = animation.FuncAnimation(fig=fig, func=update, frames=int(lifetimes_simulated*virus_duration*lerp_count/deltat), interval=100/lerp_count)

# save animation
writer = animation.PillowWriter(fps=15,
                                metadata=dict(artist='Me'),
                                bitrate=1800)
ani.save('40_masks_new.gif', writer=writer)

#plt.show()

# metrics graphing
LabelFont = {'family':'serif','color':'black','size':20}
TitleFont = {'family':'serif','color':'black','size':30}

fig_metrics, ax_metrics = plt.subplots(figsize=(10,10))
ax_metrics.set(xlim=[0, lifetimes_simulated*virus_duration], ylim=[0, len(stage_humans)])
ax_metrics.xaxis.set_tick_params(labelsize=20)
ax_metrics.yaxis.set_tick_params(labelsize=20)
ax_metrics.set_xlabel("Time (arbitrary units)", fontdict=LabelFont)
ax_metrics.set_ylabel("People", fontdict=LabelFont)
ax_metrics.set_title("Population Infection: 40% Chance of Mask", fontdict=TitleFont)

ax_metrics.fill_between(timeline, masked_healthy_count, facecolor='blue', alpha=0.15, label='Healthy Masked')
ax_metrics.plot(timeline, healthy_count, c='blue', label='Healthy')
ax_metrics.plot(timeline, dead_count, c='black', label='Dead')
ax_metrics.plot(timeline, infected_count, c='red', label='Infected')
ax_metrics.plot(timeline, immune_count, c='#11cc11', label='Immune')

ax_metrics.legend()

plt.savefig('40_masks_new.png', bbox_inches='tight') # bbox tight fixes labels getting cut off

print(f"Simulation of {len(stage_humans)} people completed in {time.time() - start_time} seconds")