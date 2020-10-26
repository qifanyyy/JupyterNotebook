#!/usr/bin/python
from __future__ import print_function

import argparse
import os.path
import platform
import subprocess
import sys

SEARCHES = [
  'branch-bound',
  'genetic-onepoint',
  'genetic-twopoint',
  'local-search',
  'simulated-annealing',
  'taboo-search',
]

PARAMETERS = {
  "amount_start_solutions": 100,
  "annealing_factor": 1.0,
  "mutation_probability": 0.05,
  "start_temperature": 30,
  "taboo_list_length": 0,
}

EXECUTABLE_FOLDERS = [
  os.path.join(os.path.dirname(__file__), 'graph-coloring', 'graph-coloring', 'bin', 'Debug'),
  os.path.join(os.path.dirname(__file__), 'graph-coloring', 'graph-coloring', 'bin', 'Release'),
  os.path.join(os.path.dirname(__file__), 'graph-coloring'),
  os.path.dirname(__file__),
]

# support functions

def get_argument(a, s):
  if hasattr(a, s):
    return getattr(a, s)
  return PARAMETERS[s]
    
# handling arguments

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--timeout", help = "timeout of algorithms in milliseconds (default 120000)", default = 120000, type = int)

search_subparsers = parser.add_subparsers(
  title = "algorithm",
  description = "search algorithm to apply (no value for all algorithms)",
  dest = "search_algorithm",
  help = "run a specific search algorithm on all test data"
)

for s in SEARCHES:
  p = search_subparsers.add_parser(
    s
  )

  # handling algorithm-specific arguments
  if s == "simulated-annealing":
    p.add_argument("-t", "--start-temperature",
      help = "start temperature to use for all simulated annealing runs (default {0})".format(PARAMETERS['start_temperature']),
      default = PARAMETERS['start_temperature'],
      type = int
    )
    p.add_argument("-f", "--annealing-factor",
      help = "annealing factor used (default {0})".format(PARAMETERS["annealing_factor"]),
      type=float,
      default = PARAMETERS["annealing_factor"]
    )
  elif s == "taboo-search":
    p.add_argument("-l", "--taboo-list-length",
      help = "length of taboo list (default amount of nodes within graph",
      type=int,
      default = PARAMETERS["taboo_list_length"]
    )
  elif s.startswith("genetic"):
    p.add_argument("-s", "--amount-start-solutions",
      type=int,
      default = PARAMETERS["amount_start_solutions"],
      help = "amount of start solutions used (default {0})".format(PARAMETERS["amount_start_solutions"])
    )
    p.add_argument("-p", "--mutation-probability",
      type=float,
      default = PARAMETERS["mutation_probability"],
      help = "probability to mutate randomly (default {0})".format(PARAMETERS["mutation_probability"])
    )

# parsing all arguments

args = parser.parse_args()

if not os.path.exists(os.path.join(os.path.dirname(__file__), 'graph_color')):
  print('Cannot find folder with test data')
  sys.exit()

EXECUTABLE_FOLDERS = [f for f in EXECUTABLE_FOLDERS if os.path.exists(os.path.join(f, 'graph-coloring.exe'))]

if len(EXECUTABLE_FOLDERS) == 0:
  print('Unable to find executable')
  sys.exit()

file = os.path.join(os.path.dirname(__file__), 'test_data.txt')

if not os.path.exists(file):
  print('Unable to find file with test data which should be run')
  sys.exit()

EXECUTABLE = os.path.join(EXECUTABLE_FOLDERS[0], 'graph-coloring.exe')

print("Using {0} to run tests".format(EXECUTABLE))

if args.search_algorithm:
  SEARCHES = [args.search_algorithm]

files = open(file, 'r').readlines()

for f in files:
  file_name = os.path.join(os.path.dirname(__file__), 'graph_color', f.strip())
  if not os.path.exists(file_name):
    print('Test file ' + file_name + ' not found.')
    continue
  for s in SEARCHES:
    print('Running ' + s + ' on ' + file_name)
    cmd_args = []
    if platform.system() != 'Windows':
      cmd_args += ['mono', '--debug']
    cmd_args += [EXECUTABLE, file_name, s, str(args.timeout)]

    # handling algorithm-specific parameters
    if s == "simulated-annealing":
      cmd_args += [str(get_argument(args, "start_temperature")), str(get_argument(args, "annealing_factor"))]
    elif s == "taboo-search" and args.taboo_list_length != 0:
      cmd_args += [str(get_argument(args, "taboo_list_length"))]
    elif s.startswith("genetic"):
      cmd_args += [str(get_argument(args, "amount_start_solutions")), str(get_argument(args, "mutation_probability"))]

    proc = subprocess.Popen(cmd_args)
    try:
      proc.communicate()

      if proc.returncode != 0:
        print("An error occurred during test, cancelling follow-ups")
        sys.exit()
    except KeyboardInterrupt:
      print('Tests interrupted')
      sys.exit()
    print('-' * 40)