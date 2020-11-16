#! /usr/bin/env python

'''
test_scenario [OPTIONS] <SCENARIO_PATH>

Test all the instances of the ASlib scenario according to the SUNNY algorithm. 
For every instance of the scenario, the corresponding SUNNY schedule is printed 
on standard output according to the AS standard format:

  instanceID,runID,solver,timeLimit

Before being tested, a scenario must be trained by using train_scenario script.

Options
=======
  -K <KB_DIR>
   Path of the SUNNY knowledge base. By default, is set to <SCENARIO_PATH>
  -s <STATIC_SCHEDULE>
   Static schedule to be run in the presolving phase for each instance of the 
   scenario. It must be specified in the form: "s_1,t_1,s_2,t_2,...,s_n,t_n"
   meaning that solver s_i has to run for t_i seconds. By default it is empty.
  -k <NEIGH.SIZE>
   The neighbourhood size of SUNNY algorithm. By default, it is set to sqrt(n) 
   where n is the size of the knowledge base.
  -P <s_1,...,s_k>
   The portfolio used by SUNNY. By default, it contains all the algorithms of 
   the scenario.
  -b <BACKUP>
   Sets the SUNNY backup solver. By default, SUNNY uses the Single Best Solver 
   of the portfolio as the backup solver.
  -T <TIMEOUT>
   Sets the timeout of SUNNY algorithm. By default, the scenario cutoff time is 
   used as timeout.
  -o <FILE>
   Prints the predicted schedules to <FILE> instead of std output.
  -f <f_1,...,f_k>
   Specifies the features to be used for solvers prediction. By default, all the 
   features resulting from the training phase (possibly pre-processed) are used.
  -m <MAX-SIZE>
   Maximum sub-portfolio size. By default, it is set to the portfolio size.
  --print-static
   Prints also the static schedule before the dynamic one computed by SUNNY.
   This options is unset by default.
  --help
   Prints this message.
'''

import os
import sys
import json
import getopt
from sunny import *

def parse_arguments(args):
  '''
  Parse the options specified by the user and returns the corresponding
  arguments properly set.
  '''
  try:
    long_options = ['help', 'print-static']
    opts, args = getopt.getopt(args, 'K:s:k:P:b:T:o:h:f:m:', long_options)
  except getopt.GetoptError as msg:
    print >> sys.stderr, msg
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)

  if not args:
    if not opts:
      print >> sys.stderr, 'Error! No arguments given.'
      print >> sys.stderr, 'For help use --help'
      sys.exit(2)
    else:
      print (__doc__)
      sys.exit(0)
      
  scenario = args[0]
  if scenario[-1] != '/':
    scenario += '/'
  if not os.path.exists(scenario):
    print >> sys.stderr, 'Error: Directory ' + scenario + ' does not exists.'
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
    
  # Initialize KB variables with default values.
  kb_path = scenario
  kb_name = kb_path.split('/')[-2]
  
  for o, a in opts:
    if o == '-K':
      if os.path.exists(a):
        kb_path = a
        if kb_path[-1] != '/':
          kb_path += '/'
        kb_name = kb_path.split('/')[-2]
      else:
        print ('Error: ' + a + ' does not exists.')
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
  # Read arguments.
  args_file = kb_path + kb_name + '.args'
  if not os.path.exists(args_file):
    print >> sys.stderr, 'Error: ' + args_file + ' does not exists.'
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
  with open(args_file, 'r') as infile:
    args = json.load(infile)
  out_file = None
  new_features = None
  print_static = False
  
  lb = args['lb']
  ub = args['ub']
  k = args['neigh_size']
  backup = args['backup']
  timeout = args['timeout']
  feat_def = args['feat_def']
  portfolio = args['portfolio']
  feature_steps = args['feature_steps']
  static_schedule = args['static_schedule']
  selected_features = args['selected_features']

  max_size = len(portfolio)
  
  # Options parsing.
  for o, a in opts:
    if o in ('-h', '--help'):
      print(__doc__)
      sys.exit(0)
    elif o == '-s':
      s = a.split(',')
      static_schedule = []
      for i in range(0, len(s) / 2):
        solver = s[2 * i]
        time = float(s[2 * i + 1])
        if time < 0:
          print >> sys.stderr, 'Error! Not acceptable negative time'
          print >> sys.stderr, 'For help use --help'
          sys.exit(2)
        static_schedule.append((solver, time))
    elif o == '-k':
      k = int(a)
    elif o == '-P':
      portfolio = a.split(',')
    elif o == '-b':
      backup = a
    elif o == '-T':
      timeout = float(a)
    elif o == '-o':
      out_file = a
    elif o == '-f':
      new_features = a.split(',')
    elif o == '-m':
      max_size = int(a)
      if max_size < 1 or max_size > len(portfolio):
        print >> sys.stderr, 'Error! Not acceptable size'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
    elif o == '--print-static':
      print_static = True
        
  if new_features:
    selected_features = dict(
      (feature, index)
      for (feature, index) in selected_features.items() 
      if feature in new_features
    )
    feature_steps = dict(
      (step, features) 
      for (step, features) in feature_steps.items()
      if set(features).intersection(new_features)
    )
    
    args_file = kb_path + kb_name + '.args'
    with open(args_file, 'r') as infile:
      args = json.load(infile)
    infile.close()
    args['selected_features'] = selected_features
    args['feature_steps'] = feature_steps
    with open(args_file, 'w') as outfile:
      json.dump(args, outfile)

  return k, lb, ub, feat_def, kb_path, kb_name, static_schedule, timeout,      \
    portfolio, backup, out_file, scenario, print_static, selected_features,    \
      feature_steps, max_size
  
def main(args):
  k, lb, ub, feat_def, kb_path, kb_name, static_schedule, timeout, portfolio,  \
    backup, out_file, scenario, print_static, selected_features, feature_steps,\
      max_size = parse_arguments(args)
  
  cost_file = scenario + 'feature_costs.arff'
  feature_costs = {}
  if os.path.exists(cost_file):
    reader = csv.reader(open(cost_file), delimiter = ',')
    for row in reader:
      steps = set([])
      i = 2
      if row and '@ATTRIBUTE' in row[0].strip().upper()  \
      and 'instance_id' not in row[0] and 'repetition' not in row[0]:
	if row[0].strip().split(' ')[1] in feature_steps.keys():
	  steps.add(i)
	i += 1
      elif row and row[0].strip().upper() == '@DATA':
	# Iterates until preamble ends.
	break
    for row in reader:
      feature_costs[row[0]] = 0
      for i in steps:
	if row[i] != '?':
	  feature_costs[row[0]] += float(row[i])
  
  reader = csv.reader(open(scenario + 'feature_values.arff'), delimiter = ',')
  for row in reader:
    if row and row[0].strip().upper() == '@DATA':
      # Iterates until preamble ends.
      break
  header = 'instanceID,runID,solver,timeLimit'
  if out_file:
    writer = csv.writer(open(out_file, 'w'), delimiter = ',')
    writer.writerow(header.split(','))
  else:
    print header
  for row in reader:
    inst = row[0]
    feat_vector = row[2:]
    if feature_costs:
      feat_cost = feature_costs[inst]
    else:
      feat_cost = 0
    # Get the schedule computed by SUNNY algorithm.
    schedule = get_sunny_schedule(
      lb, ub, feat_def, kb_path, kb_name, static_schedule, timeout, k, \
      portfolio, backup, selected_features, feat_vector, feat_cost, max_size
    )
    i = 1
    if print_static:
      schedule = static_schedule + schedule
      i = 0
    for (s, t) in schedule:
      row = inst + ',' + str(i) + ',' + s + ',' + str(t)
      if out_file:
        writer.writerow(row.split(','))
      else:
        print (row)
      i += 1
      
if __name__ == '__main__':
  main(sys.argv[1:])