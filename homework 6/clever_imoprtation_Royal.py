import numpy as np
import matplotlib.pyplot as plt
from NdimGradDescentRoyal import N_Dim_Grad_Descent_Royal

def line(x_in, m, b):
    return m*np.sin(x_in) + b

def line_1(x):
    return line(x, 50, 0.1)

def line_2(x):
    return line(x, 10, -4)

def line_3(x):
    return line(x, 3, 5)

minimum_1, steps_1, path_taken_1 = N_Dim_Grad_Descent_Royal.Ndim_grad_desc(line_1, np.array([9]), accuracy=0.000001, taken_path=True)
minimum_2, steps_2, path_taken_2 = N_Dim_Grad_Descent_Royal.Ndim_grad_desc(line_2, np.array([9]), accuracy=0.000001, taken_path=True)
minimum_3, steps_3, path_taken_3 = N_Dim_Grad_Descent_Royal.Ndim_grad_desc(line_3, np.array([9]), accuracy=0.000001, taken_path=True)

print(f"minimum of line_1 found to be {minimum_1} in {steps_1} steps.")
print(f"minimum of line_2 found to be {minimum_2} in {steps_2} steps.")
print(f"minimum of line_3 found to be {minimum_3} in {steps_3} steps.")

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

ax1.set(xlim=[0, 20], ylim=[-55,55], xlabel='x', ylabel='y', title="minimum of line_1 at the star")
ax2.set(xlim=[0, 20], ylim=[-20,20], xlabel='x', ylabel='y', title="minimum of line_2 at the star")
ax3.set(xlim=[0, 20], ylim=[0,10], xlabel='x', ylabel='y', title="minimum of line_3 at the star")

x_array = np.linspace(0, 20, 200)

ax1.plot(x_array, line_1(x_array))
ax2.plot(x_array, line_2(x_array))
ax3.plot(x_array, line_3(x_array))

ax1.scatter(minimum_1, line_1(minimum_1), marker='*')
ax2.scatter(minimum_2, line_2(minimum_2), marker='*')
ax3.scatter(minimum_3, line_3(minimum_3), marker='*')

plt.show()