'''
Usage: assign.py <filename>

A script for performing the Hungarian algorithm for solving the assignment
problem in which each task may require multiple agents.

The script takes in a csv in the following format:

,     Task 1, Task 2, Task 3, Task 4, ...
,     Cnt 1,  Cnt 2,  Cnt 3,  Cnt 4,  ...
Agt1,
Agt2,
Agt3,
.
.
.

The values in the table have been omitted for clarity.

Cnt n refers to the number of agents required to complete Task n.
'''

import csv
import munkres
import sys

'''
get_task
--------
From a list of (task, count) tuples, extracts the task at index i in a list
consisting of (count 0) copies of (task 0) followed by (count 1) copes of
(task 1), etc.
'''
def get_task(tasks, i):
  idx = 0
  for task in tasks:
    idx += task[1]
    if idx > i:
      return task[0]
  return ''

'''
First read in agents and tasks from csv
'''

if len(sys.argv) != 2:
  print 'Usage: %s <filename>' % sys.argv[0]
  exit(1)
fname = sys.argv[1]
lines = []
for row in csv.reader(open(fname, 'r')):
  lines.append(row)

agents = [lines[row][0] for row in range(2, len(lines))]

# tasks are stored as a list of (task, count) tuples.
tasks = []
for i in range(1, len(lines[1])):
  tasks.append((lines[0][i], int(lines[1][i])))

'''
Create a matrix that the Hungarian algorithm understands by creating (count n)
duplicates of each agent's value for (task n)
'''

mat = []
for i in range(2, len(lines)):
  line = lines[i]
  row = []
  for u in range(1, len(line)):
    for i in xrange(tasks[u-1][1]):
      row.append(int(line[u]))
  mat.append(row)

'''
Perform the Hungarian algorithm
'''

assignments = munkres.Munkres().compute(mat)

'''
Turn the result into a nice dictionary, mapping from task name to list of
agents
'''

res = {}
for assignment in assignments:
  task = get_task(tasks, assignment[1])
  agent = agents[assignment[0]]
  if not task in res:
    res[task] = [agent]
  else:
    res[task].append(agent)

'''
Print out the result
'''

for k, v in res.iteritems():
  print k + ': ' + ', '.join(v)

