import sys, os
import time
sys.path.append(os.pardir)
import numpy as np
from alifebook_lib.visualizers import ArrayVisualizer

# initalize Visualizer
visualizer = ArrayVisualizer()

SPACE_SIZE = 600

# binaried rule of Cellular Automata (Wolfram code)
RULE = 30

# space of CA
state = np.zeros(SPACE_SIZE, dtype=np.int8)
next_state = np.zeros(SPACE_SIZE, dtype=np.int8)

# initalize the first screen
# random
state[:] = np.random.randint(2, size=len(state))
# only center is 1, others are 0
#state[len(state)//2] = 1

while visualizer:
  for i in range(SPACE_SIZE):
    # left, center, right
    l = state[i-1]
    c = state[i]
    r = state[(i+1)%SPACE_SIZE]
    # neighbor_cell_codeは現在の状態のバイナリコーディング
    # ex) 現在が[1 1 0]の場合
    #     neighbor_cell_codeは 1*2^2 + 1*2^1 + 0*2^0 = 6となるので、
    #     RULEの６番目のビットが１ならば、次の状態は１となるので、
    #     RULEをneighbor_cell_code分だけビットシフトして１と論理積をとる。
    neighbor_cell_code = 2**2 * l + 2**1 * c + 2**0 * r
    if (RULE >> neighbor_cell_code) & 1:
      next_state[i] = 1
    else:
      next_state[i] = 0

  # swap
  state, next_state = next_state, state
  # update screen
  visualizer.update(1-state)
