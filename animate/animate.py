import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def move(x, v, t):
    return x + v*t + 0.5*accel*t**2 


positions = [np.array(x) for x in [[0,0], [0,0], [0,0]]]
vels = [np.array(x) for x in [[10,10], [15,15], [20,20]]]
toffset = [0 for v in vels]

accel = np.array([0,-9.8])
handles = list()

fig, ax = plt.subplots()

for pos in positions:
    handle = ax.scatter(pos[0], pos[1])
    handles.append(handle)

ax.set(xlim=[0, 100], ylim=[0,100], xlabel='Distance', ylabel='Height')
ax.legend()

deltat = 0.1

def update(frame):
    ax.set_title(f"{frame * deltat}")
    trim = []
    for i, pos, vel, handle, toff in zip(range(len(vels)), positions, vels, handles, toffset):
        new_pos = move(pos, vel, (frame - toff) * deltat)
        handle.set_offsets([new_pos[0], new_pos[1]])
        if new_pos[1] < 0:
            trim.append(i)
    for i in trim:
        positions.pop(i)
        vels.pop(i)
        toffset.pop(i)
        handles[i].remove()
        handles.pop(i)

    if frame % 20 == 0:
        positions.append(np.array([0,0]))
        vels.append(np.abs(np.random.randn(2)*20))
        toffset.append(frame)
        handle = ax.scatter([0], [0])
        handles.append(handle)

ani = animation.FuncAnimation(fig=fig, func=update, frames=50, interval=100)

# writer = animation.PillowWriter(fps=15,
#                                 metadata=dict(artist='Me'),
#                                 bitrate=1800)
# ani.save('scatter.gif', writer=writer)
plt.show()