import numpy as np



def partial_deriv_central(f, x0, delta=1e-8):
    dimensions = len(x0)
    fpartial = np.zeros(dimensions)

    for i in range(dimensions):
        partial_delta = np.zeros(dimensions)
        partial_delta[i] = delta
        fpartial[i] = (f(x0 + partial_delta) - f(x0 - partial_delta)) / (2*delta)

    gradient = np.linalg.norm(fpartial) # epic way to get vector magnitude

    return fpartial, gradient


def Ndim_grad_desc(f, x0, step=0.01, accuracy=0.0001, verbose=False, counting=True, max_steps=10000, deriv_delta=1e-8, taken_path=False):
    fpartial, gradient = partial_deriv_central(f, x0, delta=deriv_delta)
    step_count = 0
    points_checked = [x0.tolist() + [float(f(x0))]]
    while np.abs(gradient) > accuracy:
        fpartial, gradient = partial_deriv_central(f, x0, delta=deriv_delta)
        
        x0 = x0 - fpartial*step
        if verbose:
            print(x0, fpartial, step)
        if counting:
            step_count +=1
            if step_count == max_steps+1:
                print(f"Exceeded maximum steps ({max_steps}).  Current output is:")
                break
        if taken_path:
            points_checked.append(x0.tolist() + [float(f(x0))])
    return x0, step_count, np.array(points_checked).T