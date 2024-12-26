from scl_utils import *


def production(particles, x, y, probability):
  p = particles[x, y]
  # select two neighbor particles in random
  n0_x, n0_y, n1_x, n1_y = get_random_2_moore_neighborhood(x,y,particles.shape[0])
  n0_p = particles[n0_x, n0_y]
  n1_p = particles[n1_x, n1_y]
  if p['type'] != 'CATALYST' or n0_p['type'] != 'SUBSTRATE' or n1_p['type'] != 'SUBSTRATE':
    return
  if evaluate_probability(probability):
    n0_p['type'] = 'HOLE'
    n1_p['type'] = 'LINK'


def disintegration(particles, x, y, probability):
  p = particles[x, y]
  # if disintegration can't be occured because there are no room at the neighbor, the flag admin the disintegration status
  if p['type'] in ('LINK', 'LINK_SUBSTRATE') and evaluate_probability(probability):
    p['disintegrating_flag'] = True

  if not p['disintegrating_flag']:
    return
  
  # if LINK include SUBSTRATE, it is forced to emit. so call emission with 1.0 probability 
  emission(particles, x, y, 1.0)

  # select neighbor particle in random
  n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
  n_p = particles[n_x, n_y]
  if p['type'] == 'LINK' and n_p['type'] == 'HOLE': 
    # case that there are enough space at the neighbor for disintegration

    # call bond_decay with 1.0 probability to delete all bond
    bond_decay(particles, x, y, 1.0)
    # execute disintegration
    p['type'] = 'SUBSTRATE'
    n_p['type'] = 'SUBSTRATE'
    p['disintegrating_flag'] = False


def bonding(particles, x, y, chain_initiate_probability, chain_splice_probability, chain_extend_probability, chain_inhabit_bond_flag=True,catalyst_inhibit_bond_flag=True):
  p = particles[x,y]

  # select neighbor particle in random
  n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
  # check the type, the number of bonds, angle and across of the two particles 
  n_p = particles[n_x, n_y]
  # check the type
  if not p['type'] in ('LINK', 'LINK_SUBSTRATE'):
    return
  if not n_p['type'] in ('LINK', 'LINK_SUBSTRATE'):
    return
  # check already bonding
  if (n_x, n_y) in p['bonds']:
    return
  # check the number of bonds
  if len(p['bonds']) >= 2 or len(n_p['bonds']) >= 2:
    return
  # check angle and across
  an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(x, y, n_x, n_y, particles.shape[0])
  if (an0_x, an0_y) in p['bonds'] or (an1_x, an1_y) in p['bonds']:
    return
  an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(n_x, n_y, x, y, particles.shape[0])
  if (an0_x, an0_y) in n_p['bonds'] or (an1_x, an1_y) in n_p['bonds']:
    return
  an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(x, y, n_x, n_y, particles.shape[0])
  if (an0_x, an0_y) in particles[an1_x, an1_y]['bonds']:
    return 
  
  # option check 
  # 1 case exist particle which already bond with other particle at moore neighbor
  # 2 case exist catalyst at moore neighbor
  mn_list = get_moore_neighborhood(x, y, particles.shape[0]) + get_moore_neighborhood(n_x, n_y, particles.shape[0])
  if catalyst_inhibit_bond_flag:
    for mn_x, mn_y in mn_list:
      if particles[mn_x, mn_y]['type'] == 'CATALYST':
        return
  if chain_inhabit_bond_flag:
    for mn_x, mn_y in mn_list:
      if len(particles[mn_x, mn_y]['bonds']) >= 2:
        if not (x, y) in particles[mn_x, mn_y]['bonds'] and not (n_x, n_y) in particles[mn_x, mn_y]['bonds']:
          return


  # execute bonding
  if len(p['bonds']) == 0 and len(n_p['bonds']) == 0:
    prob = chain_initiate_probability
  elif len(p['bonds']) == 1 and len(n_p['bonds']) == 1:
    prob = chain_splice_probability
  else:
    prob = chain_extend_probability

  if evaluate_probability(prob):
    p['bonds'].append((n_x, n_y))
    n_p['bonds'].append((x, y))



def bond_decay(particles, x, y, probability):
  p = particles[x, y]
  if p['type'] in ('LINK', 'LINK_SUBSTRATE') and evaluate_probability(probability):
    for b in p['bonds']:
      particles[b[0], b[1]]['bonds'].remove((x, y))
    p['bonds'] = []

def absorption(particles, x, y, probability):
  p = particles[x, y]
  # select neighbor particle in random
  n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
  n_p = particles[n_x, n_y]
  if p['type'] != 'LINK' or n_p['type'] != 'SUBSTRATE':
    return
  if evaluate_probability(probability):
    p['type'] = 'LINK_SUBSTRATE'
    n_p['type'] = 'HOLE'

def emission(particles, x, y, probability):
  p = particles[x, y]
  # select neighbor particle in random
  n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
  n_p = particles[n_x, n_y]
  if p['type'] != 'LINK_SUBSTRATE' or n_p['type'] != 'HOLE':
    return
  if evaluate_probability(probability):
    p['type'] = 'LINK'
    n_p['type'] = 'SUBSTRATE'

