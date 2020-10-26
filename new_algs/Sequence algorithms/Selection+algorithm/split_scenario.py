#! /usr/bin/env python

'''
split_scenario [OPTIONS] <SCENARIO_PATH>

Given the scenario path, creates 2 * N * M folders where N is the number of the 
repetition and M the number of folds of the scenario. For i = 1, ..., N and 
j = 1, ..., M each folder is called train_i_j (resp. test_i_j) and consists in a 
clone of the original scenario which only contains the training (resp. test)
instances of the scenario.

Options
=======
  --name <NAME>
    Name of the folder containing the train/test sub-folders. The default name 
    is cv_<SCENARIO>, where <SCENARIO> is the name of the folder containing the 
    given scenario.
  --path <PATH>
    Creates the cv folders at the specified path. By default, <PATH> is set to 
    the scenario path.
  --random-split
    (TBD)
    Creates a random splitting of the training and test sets (by using the same 
    number of repetition and folds). This option is unset by default.
  --help
   Prints this message.
'''

import os
import sys
import csv
import getopt
import shutil

def parse_arguments(args):
  '''
  Parse the options specified by the user and returns the corresponding
  arguments properly set.
  '''
  try:
    options = ['help', 'name=', 'path=', 'random-split=']
    opts, args = getopt.getopt(args, None, options)
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
      print __doc__
      sys.exit(0)

  scenario = args[0]
  if scenario[-1] != '/':
    scenario += '/'
  if not os.path.exists(scenario):
    print >> sys.stderr, 'Error: Directory ' + scenario + ' does not exists.'
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
    
  # Initialize variables with default values.
  random = False
  cv_path = scenario
  cv_name = 'cv_' + scenario.split('/')[-2]

  # Options parsing.
  for o, a in opts:
    if o == '--help':
      print __doc__
      sys.exit(0)
    elif o == '--random-split':
      discard = True
    elif o == '--path':
      if not os.path.exists(a):
        print >> sys.stderr, 'Error! Directory ' + a + ' not exists.'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
      if a[-1] == '/':
        cv_path = a[:-1]
      else:
        cv_path = a
    elif o == '--name':
      cv_name = a

  cv_dir = cv_path + '/' + cv_name + '/'
  if not os.path.exists(cv_dir):
    os.makedirs(cv_dir)
  else:
    print >> sys.stderr, 'Warning! Directory ' + cv_dir + ' already exists.'

  return scenario, cv_dir, random

def main(args):
  scenario, cv_dir, random = parse_arguments(args)
  reader = csv.reader(open(scenario + 'cv.arff'), delimiter = ',')
  for row in reader:
    if row and row[0].strip().upper() == '@DATA':
      # Iterates until preamble ends.
      break
  cv = {}
  for row in reader:
    if len(row) < 3:
      continue
    rep = row[1]
    fold = row[2]
    if rep not in cv.keys():
      cv[rep] = {}
    if fold not in cv[rep].keys():
      cv[rep][fold] = set([])
    cv[rep][fold].add(row[0])
  num_reps = len(cv)
  num_folds = len(cv.values()[0])
  if random:
    # TBD: Implement this.
    pass
  for i in range(1, num_reps + 1):
    i = str(i)
    for j in range(1, num_folds + 1):
      j = str(j)
      train_dir = cv_dir + 'train_' + i + '_' + j + '/'
      os.makedirs(train_dir)
      test_dir = cv_dir + 'test_' + i + '_' + j + '/'
      os.makedirs(test_dir)
      shutil.copyfile(
        scenario + 'description.txt', train_dir + 'description.txt'
      )
      for infile in [
        'algorithm_runs.arff', 'feature_values.arff', 'feature_costs.arff'
      ]:
	if not os.path.exists(scenario + infile):
	  continue
        reader = csv.reader(open(scenario + infile), delimiter = ',')
        writer_train = csv.writer(open(train_dir + infile, 'w'))
        writer_test = csv.writer(open(test_dir + infile, 'w'))
        for row in reader:
	  writer_train.writerow(row)
          writer_test.writerow(row)
          if row and row[0].strip().upper() == '@DATA':
            # Iterates until preamble ends.
            break
        for row in reader:
          if row[0] in cv[i][j]:
            writer_test.writerow(row)
          else:
            writer_train.writerow(row)

if __name__ == '__main__':
  main(sys.argv[1:])