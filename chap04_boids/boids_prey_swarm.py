import sys, os
import time
sys.path.append(os.pardir)
import numpy as np
from swarm_with_prey_visualizer import SwarmVisualizer


# initialize visualizer
visualizer = SwarmVisualizer()

# simulation parameter
N = 256
PN = 256
FN = 1

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



# max and min of velocity
MIN_VEL = 0.005
MAX_VEL = 0.03

# force at boundary (if this value = 0, free boundary)
BOUNDARY_FORCE = 0.001

# the force of attracting to pray 
#ATTRACT_FORCE = 0.0005
#ATTRACT_FORCE = 0.005
ATTRACT_FORCE = 0.05
ATTRACT_DISTANCE = 0.5
ATTRACT_ANGLE = np.pi / 1

# the parameter of escaping from predator
#ESCAPE_FORCE = 0.0001
#ESCAPE_FORCE = 0.001
ESCAPE_FORCE = 0.05
#ESCAPE_DISTANCE = 0.05
ESCAPE_DISTANCE = 0.1
ESCAPE_ANGLE = np.pi / 1

# the force of attracting to feed and the step of feed moving
FEED_FORCE = 0.0005
#FEED_FORCE = 0.05
#FEED_MOVEMENT_STEP = 150
FEED_MOVEMENT_STEP = 450


def main():

  # init position and velocity
  # random between [-1, 1) * 3 dimention
  x = np.random.rand(N, 3) * 2 - 1
  v = (np.random.rand(N, 3) * 2 - 1 ) * MIN_VEL
  
  # prey position and velocity
  px = np.random.rand(PN, 3) * 2 - 1
  pv = (np.random.rand(PN, 3) * 2 - 1 ) * MIN_VEL
  
  # feed position
  FN = 1
  fx = np.random.rand(FN, 3) * 2 - 1
  
  # force variable of cohesion, separation, alignment
  dv_coh = np.empty((N,3))
  dv_sep = np.empty((N,3))
  dv_ali = np.empty((N,3))
  # boundary force variable
  dv_boundary = np.empty((N,3))
  
  
  # force variable of cohesion, separation, alignment for prey
  dpv_coh = np.empty((N,3))
  dpv_sep = np.empty((N,3))
  dpv_ali = np.empty((N,3))
  # boundary force variable for prey
  dpv_boundary = np.empty((N,3))

  # attracting velocity
  dv_attract_to_prey = np.empty((N,3))

  # escaping velocity
  dpv_escape_from_predator = np.empty((N,3))

  # loop
  t = 0
  while visualizer:
  
    #time.sleep(0.05)
    #time.sleep(0.01)
  
    # calc delta in velocity and update velocity
    calc_dv(N, x, v, dv_coh, dv_sep, dv_ali, dv_boundary)
    v += dv_coh + dv_sep + dv_ali + dv_boundary
  
    # calc delta in prey velocity
    calc_dv(PN, px, pv, dpv_coh, dpv_sep, dpv_ali, dpv_boundary)
    pv += dpv_coh + dpv_sep + dpv_ali + dpv_boundary
  
    # attracting to prey
    for i in range(N):
      x_this = x[i]
      v_this = v[i]
      distance = np.linalg.norm(px - x_this, axis=1)
      angle = np.arccos(np.dot(v_this, (px-x_this).T) / (np.linalg.norm(v_this) * np.linalg.norm((px-x_this), axis=1)))
      attract_agents_px = px[ (distance < ATTRACT_DISTANCE) & (angle < ATTRACT_ANGLE) ]
      dv_attract_to_prey[i] = ATTRACT_FORCE * (np.average(attract_agents_px, axis=0) - x_this) if (len(attract_agents_px) > 0) else 0
    v += dv_attract_to_prey
  
    # atracting to feed
    pv += FEED_FORCE * (fx - px) / np.linalg.norm((fx - px), axis=1, keepdims=True)**2
 
    # escaping from predator
    for i in range(PN):
      px_this = px[i]
      pv_this = pv[i]
      distance = np.linalg.norm(x - px_this, axis=1)
      angle = np.arccos(np.dot(pv_this, (x-px_this).T) / (np.linalg.norm(pv_this) * np.linalg.norm((x-px_this), axis=1)))
      escape_agents_x = x[ (distance < ESCAPE_DISTANCE) & (angle < ESCAPE_ANGLE) ]
      dpv_escape_from_predator[i] = ESCAPE_FORCE * np.sum(px_this - escape_agents_x, axis=0) if (len(escape_agents_x) > 0) else 0
    pv += dpv_escape_from_predator


    if t % FEED_MOVEMENT_STEP == 0:
      fx = np.random.rand(FN, 3) * 2 - 1
      visualizer.set_markers(fx)
    t += 1
  
    adjust_velocity(N, v)
    adjust_velocity(PN, pv)
  
    # update position
    x += v
    px += pv
    
    visualizer.update(x, v)
    visualizer.update2(px, pv)





def calc_dv(n, x, v, dv_coh, dv_sep, dv_ali, dv_boundary):

  for i in range(n):
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


def adjust_velocity(n, v):

  for i in range(n):
    v_abs = np.linalg.norm(v[i])
    if (v_abs < MIN_VEL):
      v[i] = MIN_VEL * v[i] / v_abs
    elif (v_abs > MAX_VEL):
      v[i] = MAX_VEL * v[i] / v_abs






if __name__ == '__main__':
  main()

