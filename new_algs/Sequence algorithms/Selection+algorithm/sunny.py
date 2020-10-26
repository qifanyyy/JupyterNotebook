'''
Helper module for computing the SUNNY schedule.
'''

import csv
import json
from math import sqrt
from combinations import binom, get_subset

def normalize(feat_vector, selected_features, lims, inf, sup, def_feat_value):
  """
  Normalizes the feature vector in input in the range [inf, sup]
  """
  norm_vector = []
  for i in selected_features:
    lb = lims[str(i)][0]
    ub = lims[str(i)][1]
    f = feat_vector[i]
    if f == '?':
      f = def_feat_value
    else:
      f = float(f)
      if f < lb:
        f = inf
      elif f > ub:
        f = sup
      else:
	if ub - lb != 0:
          x = (f - lb) / (ub - lb)
          f = inf + (sup - inf) * x
        else:
	  f = def_feat_value
        assert inf <= f <= sup
    norm_vector.append(f)
  return norm_vector


def get_neighbours(feat_vector, selected_features, kb, k):
  """
  Returns a dictionary (inst_name, inst_info) of the k instances closer to the 
  feat_vector in the knowledge base kb.
  """
  reader = csv.reader(open(kb, 'r'), delimiter = '|')
  infos = {}
  distances = []
  for row in reader:
    inst = row[0]
    ori_vector = map(float, row[1][1 : -1].split(','))
    d = euclidean_distance(
      feat_vector, [ori_vector[i] for i in selected_features]
    )
    distances.append((d, inst))
    infos[inst] = row[2]
  distances.sort(key = lambda x : x[0])
  return dict((inst, infos[inst]) for (d, inst) in distances[0 : k])


def euclidean_distance(fv1, fv2):
  """
  Computes the Euclidean distance between two feature vectors fv1 and fv2.
  """
  assert len(fv1) == len(fv2)
  distance = 0.0
  for i in range(0, len(fv1)):
    d = fv1[i] - fv2[i]
    distance += d * d
  return sqrt(distance)


def get_schedule(neighbours, timeout, portfolio, k, backup, max_size):
  """
  Returns the corresponding SUNNY schedule.
  """
 
  # Dictionaries for keeping track of the instances solved and the runtimes. 
  solved = {}
  times  = {}
  for solver in portfolio:
    solved[solver] = set([])
    times[solver]  = 0.0
  for inst, item in neighbours.items():
    item = eval(item)
    for solver in portfolio:
      time = item[solver]['time']
      if time < timeout:
        solved[solver].add(inst)
      times[solver] += time
  # Select the best sub-portfolio, i.e., the one that allows to solve more 
  # instances in the neighborhood.
  max_solved = 0
  min_time = float('+inf')
  best_pfolio = []
  m = max_size
  for i in range(1, m + 1):
    old_pfolio = best_pfolio
    
    for j in range(0, binom(m, i)):
      solved_instances = set([])
      solving_time = 0
      # get the (j + 1)-th subset of cardinality i
      sub_pfolio = get_subset(j, i, portfolio)
      for solver in sub_pfolio:
        solved_instances.update(solved[solver])
        solving_time += times[solver]
      num_solved = len(solved_instances)
      
      if num_solved >  max_solved or \
        (num_solved == max_solved and solving_time < min_time):
          min_time = solving_time
          max_solved = num_solved
          best_pfolio = sub_pfolio
          
    if old_pfolio == best_pfolio:
      break
    
  # n is the number of instances solved by each solver plus the instances 
  # that no solver can solver.
  n = sum([len(solved[s]) for s in best_pfolio]) + (k - max_solved)
  schedule = {}
  # Compute the schedule and sort it by number of solved instances.
  for solver in best_pfolio:
    ns = len(solved[solver])
    if ns == 0 or round(timeout / n * ns) == 0:
      continue
    schedule[solver] = timeout / n * ns
  
  tot_time = sum(schedule.values())
  # Allocate to the backup solver the (eventual) remaining time.
  if round(tot_time) < timeout:
    if backup in schedule.keys():
      schedule[backup] += timeout - tot_time
    else:
      schedule[backup]  = timeout - tot_time
  sorted_schedule = sorted(schedule.items(), key = lambda x: times[x[0]])
  #assert sum(t for (s, t) in sorted_schedule) - timeout < 0.001
  return sorted_schedule

def get_sunny_schedule(
  lb, ub, def_feat_value, kb_path, kb_name, static_schedule, timeout, k, \
  portfolio, backup, selected_features, feat_vector, feat_cost, max_size
):
  selected_features = sorted(selected_features.values())
  with open(kb_path + kb_name + '.lims') as infile:
    lims = json.load(infile)
  
  norm_vector = normalize(
    feat_vector, selected_features, lims, lb, ub, def_feat_value
  )
  kb = kb_path + kb_name + '.info'
  neighbours = get_neighbours(norm_vector, selected_features, kb, k)
  timeout -= feat_cost + sum(t for (s, t) in static_schedule)
  if timeout > 0: 
    return get_schedule(neighbours, timeout, portfolio, k, backup, max_size)
  else:
    return []