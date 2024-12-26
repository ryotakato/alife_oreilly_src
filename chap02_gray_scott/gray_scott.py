import sys, os
import time
sys.path.append(os.pardir)
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer

# initalize Visualizer
visualizer = MatrixVisualizer()

SPACE_GRID_SIZE = 256
dx = 0.01 # density (roughness), so SPACE_GRID_SIZE * dx = space length
dt = 1 # calculation time is equivalent to simulation time
VISUALIZATION_STEP = 8 # step per updating screen

# diffusion constant
Du = 2e-5
Dv = 1e-5
# feed, kill constant
f, k = 0.022, 0.051 # stripe
#f, k = 0.04, 0.06 # amorphous
#f, k = 0.035, 0.065 # spots
#f, k = 0.012, 0.05 # wandering bubbles
#f, k = 0.025, 0.05 # waves

# initalize of density
u = np.ones((SPACE_GRID_SIZE, SPACE_GRID_SIZE))
v = np.zeros((SPACE_GRID_SIZE, SPACE_GRID_SIZE))

# locate SQUARE_SIZE scuare
SQUARE_SIZE = 20
square_start = SPACE_GRID_SIZE//2 - SQUARE_SIZE//2
square_end = SPACE_GRID_SIZE//2 + SQUARE_SIZE//2
u[square_start:square_end,
  square_start:square_end] = 0.5
v[square_start:square_end,
  square_start:square_end] = 0.25

# noise for breaking symmetry
# rand function is [0, 1) so, this value is addition [0, 0.1)
u += np.random.rand(SPACE_GRID_SIZE, SPACE_GRID_SIZE) * 0.1
v += np.random.rand(SPACE_GRID_SIZE, SPACE_GRID_SIZE) * 0.1

while visualizer:

  for i in range(VISUALIZATION_STEP):
    # calculation of laplacian
    # the reason which divide by dx*dx is to express distance per time
    laplacian_u = (np.roll(u, 1, axis=0) + np.roll(u, -1, axis=0) +
                   np.roll(u, 1, axis=1) + np.roll(u, -1, axis=1) - 4*u) / (dx*dx)
    laplacian_v = (np.roll(v, 1, axis=0) + np.roll(v, -1, axis=0) +
                   np.roll(v, 1, axis=1) + np.roll(v, -1, axis=1) - 4*v) / (dx*dx)

    # Gray-Scott model equation
    dudt = Du*laplacian_u - u*v*v + f*(1.0-u)
    dvdt = Dv*laplacian_v + u*v*v - (f+k)*v
    u += dt * dudt
    v += dt * dvdt

  #time.sleep(0.5)

  visualizer.update(u)

