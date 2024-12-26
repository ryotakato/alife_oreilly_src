import sys, os
import time
sys.path.append(os.pardir)
import numpy as np
from alifebook_lib.visualizers import SwarmVisualizer


# initialize visualizer
visualizer = SwarmVisualizer()

# simulation parameter
N = 256

# init pattern
# strength of force
COHESION_FORCE = 0.008
SEPARATION_FORCE = 0.4
ALIGNMENT_FORCE = 0.06
# distance of force
COHESION_DISTANCE = 0.5
SEPARATION_DISTANCE = 0.05
ALIGNMENT_DISTANCE = 0.1
# angle of force
COHESION_ANGLE = np.pi / 2
SEPARATION_ANGLE = np.pi / 2
ALIGNMENT_ANGLE = np.pi / 3



## swarm pattern
## strength of force
#COHESION_FORCE = 0.2
#SEPARATION_FORCE = 0.10
#ALIGNMENT_FORCE = 0.03
## distance of force
#COHESION_DISTANCE = 0.5
#SEPARATION_DISTANCE = 0.08
#ALIGNMENT_DISTANCE = 0.1
## angle of force
#COHESION_ANGLE = np.pi / 2
#SEPARATION_ANGLE = np.pi / 2
#ALIGNMENT_ANGLE = np.pi / 3


# torus pattern
## strength of force
#COHESION_FORCE = 0.005
#SEPARATION_FORCE = 0.5
#ALIGNMENT_FORCE = 0.01
## distance of force
#COHESION_DISTANCE = 0.8
#SEPARATION_DISTANCE = 0.03
#ALIGNMENT_DISTANCE = 0.5
## angle of force
#COHESION_ANGLE = np.pi / 2
#SEPARATION_ANGLE = np.pi / 2
#ALIGNMENT_ANGLE = np.pi / 2

## dynamic parallel group
## strength of force
#COHESION_FORCE = 0.008
#SEPARATION_FORCE = 0.5
#ALIGNMENT_FORCE = 0.05
## distance of force
#COHESION_DISTANCE = 0.2
#SEPARATION_DISTANCE = 0.04
#ALIGNMENT_DISTANCE = 0.3
## angle of force
#COHESION_ANGLE = np.pi / 2
#SEPARATION_ANGLE = np.pi / 2
#ALIGNMENT_ANGLE = np.pi / 2


## highly parallel group
## strength of force
#COHESION_FORCE = 0.002
#SEPARATION_FORCE = 0.5
#ALIGNMENT_FORCE = 0.01
## distance of force
#COHESION_DISTANCE = 0.8
#SEPARATION_DISTANCE = 0.05
#ALIGNMENT_DISTANCE = 0.5
## angle of force
#COHESION_ANGLE = np.pi
#SEPARATION_ANGLE = np.pi / 2
#ALIGNMENT_ANGLE = np.pi / 2



## original pattern
## strength of force
#COHESION_FORCE = 0.2
#SEPARATION_FORCE = 0.10
#ALIGNMENT_FORCE = 0.05
## distance of force
#COHESION_DISTANCE = 0.08
#SEPARATION_DISTANCE = 0.1
#ALIGNMENT_DISTANCE = 0.3
## angle of force
#COHESION_ANGLE = np.pi / 2
#SEPARATION_ANGLE = np.pi / 2
#ALIGNMENT_ANGLE = np.pi / 2



## original random pattern
## strength of force
#COHESION_FORCE = 0.8
#SEPARATION_FORCE = 0.9
#ALIGNMENT_FORCE = 0.40
## distance of force
#COHESION_DISTANCE = 0.6
#SEPARATION_DISTANCE = 0.01
#ALIGNMENT_DISTANCE = 0.2
## angle of force
#COHESION_ANGLE = np.pi / 4
#SEPARATION_ANGLE = np.pi / 7
#ALIGNMENT_ANGLE = np.pi / 5



# max and min of velosity
MIN_VEL = 0.005
MAX_VEL = 0.03

# force at boundary (if this value = 0, free boundary)
BOUNDARY_FORCE = 0.001

# the force of atracting to prey and the step of prey moving
PREY_FORCE = 0.0005
PREY_MOVEMENT_STEP = 150



# init position and velosity
# random between [-1, 1) * 3 dimention
x = np.random.rand(N, 3) * 2 - 1
v = (np.random.rand(N, 3) * 2 - 1 ) * MIN_VEL

# prey position
PN = 1
prey_x = np.random.rand(PN, 3) * 2 - 1


# force variable of cohesion, separation, alignment
dv_coh = np.empty((N,3))
dv_sep = np.empty((N,3))
dv_ali = np.empty((N,3))
# boundary force variable
dv_boundary = np.empty((N,3))


t = 0
while visualizer:

  #time.sleep(0.05)
  #time.sleep(0.01)

  for i in range(N):
    # target individual
    x_this = x[i]
    v_this = v[i]
    # other individual
    x_that = np.delete(x, i, axis=0)
    v_that = np.delete(v, i, axis=0)
    # distance(Euclidean distance) and angle between individual
    distance = np.linalg.norm(x_that - x_this, axis=1)
    angle = np.arccos(np.dot(v_this, (x_that-x_this).T) / (np.linalg.norm(v_this) * np.linalg.norm((x_that-x_this), axis=1)))

    # individual list in the entent which various force work
    coh_agents_x = x_that[ (distance < COHESION_DISTANCE) & (angle < COHESION_ANGLE) ]
    sep_agents_x = x_that[ (distance < SEPARATION_DISTANCE) & (angle < SEPARATION_ANGLE) ]
    ali_agents_v = v_that[ (distance < ALIGNMENT_DISTANCE) & (angle < ALIGNMENT_ANGLE) ]
    # calculation of various force
    dv_coh[i] = COHESION_FORCE * (np.average(coh_agents_x, axis=0) - x_this) if (len(coh_agents_x) > 0) else 0
    dv_sep[i] = SEPARATION_FORCE * np.sum(x_this - sep_agents_x, axis=0) if (len(sep_agents_x) > 0) else 0
    dv_ali[i] = ALIGNMENT_FORCE * (np.average(ali_agents_v, axis=0) - v_this) if (len(ali_agents_v) > 0) else 0
    # distance from the origin
    dist_center = np.linalg.norm(x_this)
    dv_boundary[i] = - BOUNDARY_FORCE * x_this * (dist_center - 1) / dist_center if (dist_center > 1) else 0

  # update velosity (and check the max and min)
  v += dv_coh + dv_sep + dv_ali + dv_boundary

  # atracting to prey
  v += PREY_FORCE * (prey_x - x) / np.linalg.norm((prey_x - x), axis=1, keepdims=True)**2

  if t % PREY_MOVEMENT_STEP == 0:
    prey_x = np.random.rand(PN, 3) * 2 - 1
    visualizer.set_markers(prey_x)
  t += 1

  for i in range(N):
    v_abs = np.linalg.norm(v[i])
    if (v_abs < MIN_VEL):
      v[i] = MIN_VEL * v[i] / v_abs
    elif (v_abs > MAX_VEL):
      v[i] = MAX_VEL * v[i] / v_abs

  # update position
  x += v
  
  visualizer.update(x, v)


