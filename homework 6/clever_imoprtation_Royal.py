import numpy as np
from NdimGradDescentRoyal import N_Dim_Grad_Descent_Royal

def line(x_in, m, b):
    return m*np.sin(x_in) + b

def line_2(x):
    return line(x, 10, 0.1)

minimum, steps, path_taken = N_Dim_Grad_Descent_Royal.Ndim_grad_desc(line_2, np.array([9]), accuracy=0.000001, taken_path=True)

print(f"minimum found to be {minimum} in {steps} steps.")