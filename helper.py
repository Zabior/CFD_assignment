import numpy as np
import math
from scipy.optimize import minimize

def ymin_from_r(r, L, N):
    return L * (r - 1) / (r**(N-1) - 1)

def r_from_ymin(ymin, L, N):
    res = minimize(lambda rr: abs(ymin_from_r(rr, L, N) - ymin),
                   x0=1.0,
                   bounds=[(1.0, 1.2)],
                   method='Nelder-Mead'
                   )
    return res.x[0]

if __name__ == "__main__":
    L = 0.2
    N = 48
    ymin = 4.2e-4
    print(r_from_ymin(ymin, L, N))