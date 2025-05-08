import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

people = np.array([25, 50, 50, 75, 
                   100, 100, 100, 125, 
                   150, 175, 200])
time = np.array([63.975945711135864, 84.25355935096741, 91.17434024810791, 126.75098586082458, 
                 143.42648696899414, 135.8740622997284, 138.9078209400177, 189.07688283920288, 
                 196.82082796096802, 231.3089680671692, 282.85116815567017])

def linear(x, m, b):
    return m*x + b

def quadratic(x, a, b, c):
    return a*x**2 + b*x + c

people_line = np.arange(0, 200, 1)
linear_param = curve_fit(linear, people, time)
quadratic_param = curve_fit(quadratic, people, time)
def linear_fit(x):
    return linear(x, linear_param[0][0], linear_param[0][1])
def quadratic_fit(x):
    return quadratic(x, quadratic_param[0][0], quadratic_param[0][1], quadratic_param[0][2])


LabelFont = {'family':'serif','color':'black','size':20}
TitleFont = {'family':'serif','color':'black','size':30}

fig, ax = plt.subplots(figsize=(10,10))
ax.set(xlim=[0, 200], ylim=[0, 300])
ax.xaxis.set_tick_params(labelsize=20)
ax.yaxis.set_tick_params(labelsize=20)
ax.set_xlabel("People", fontdict=LabelFont)
ax.set_ylabel("Time (s)", fontdict=LabelFont)
ax.set_title("Simulation Time vs Population Size", fontdict=TitleFont)


ax.plot(people_line, linear_fit(people_line), label='linear fit', c='#dddd00')
ax.plot(people_line, quadratic_fit(people_line), label='quadratic fit', c='#11cc11')
ax.scatter(people, time, c=time, cmap='cool', s=40)

ax.legend()

plt.savefig('sim_times.png', bbox_inches='tight') # bbox tight fixes labels getting cut off