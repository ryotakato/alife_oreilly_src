import sys, os
import time
sys.path.append(os.pardir)
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer

# pattern
STATIC = np.array(
[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [1,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1,1,0],
 [1,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1],
 [0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,1,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
])

OSCILLATOR = np.array(
[[1,0,0,0,0,1,0,0],
 [1,0,0,0,1,0,0,1],
 [1,0,0,0,1,0,0,1],
 [0,0,0,0,0,0,1,0]])

GLIDER = np.array(
[[0,0,0,0],
 [0,0,1,0],
 [0,0,0,1],
 [0,1,1,1]])


GLIDER_GUN = np.array(
[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
 [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
 [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])


# initalize Visualizer
visualizer = MatrixVisualizer()

WIDTH = 50
HEIGHT = 50

# state of game of life
state = np.zeros((HEIGHT, WIDTH), dtype=np.int8)
next_state = np.empty((HEIGHT, WIDTH), dtype=np.int8)

# initalize the first screen
# random
#state = np.random.randint(2, size=(HEIGHT,WIDTH), dtype=np.int8)
# pattern
#pattern = STATIC
#pattern = OSCILLATOR
pattern = GLIDER
#pattern = GLIDER_GUN
state[2:2+pattern.shape[0], 2:2+pattern.shape[1]] = pattern

#time.sleep(5)
while visualizer:
  for i in range(HEIGHT):
    for j in range(WIDTH):
      # get own and surrounging cell state
      # c: center (myself)
      # nw: north west, ne: north east, c: center ...
      nw = state[i-1, j-1]
      n  = state[i-1, j]
      ne = state[i-1, (j+1)%WIDTH]
      w  = state[i, j-1]
      c  = state[i, j]
      e  = state[i, (j+1)%WIDTH]
      sw = state[(i+1)%HEIGHT, j-1]
      s  = state[(i+1)%HEIGHT, j]
      se = state[(i+1)%HEIGHT, (j+1)%WIDTH]
      neighbor_cell_sum = nw + n + ne + w + e + sw + s + se
      if c == 0 and neighbor_cell_sum == 3:
        next_state[i, j] = 1
      elif c == 1 and neighbor_cell_sum in (2,3):
        next_state[i, j] = 1
      else:
        next_state[i, j] = 0

  time.sleep(0.1)

  # swap
  state, next_state = next_state, state
  # update screen
  visualizer.update(1-state)
