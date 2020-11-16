from munkres import Munkres, print_matrix, make_cost_matrix, DISALLOWED
import numpy as np
import sys

mentors = ['Ramy Farid', "Jennifer Daniel", "Robert Abel", "Lingle Wang"]
mentors = {x[1]: x[0] for x in enumerate(mentors)}
mentees = ["Shi-Yi", 'Ed Harder', "Cony D'Cruz", "Leah Frye", "Matt Halls"]
mentees = {x[1]: x[0] for x in enumerate(mentees)}
matrix = [[1] * len(mentees) for x in mentors]

# Disallow and Boost Edges
# Setup network based on your findings
matrix[mentors["Jennifer Daniel"]][mentees["Leah Frye"]] = 2
matrix[mentors['Robert Abel']][mentees['Ed Harder']] = DISALLOWED
matrix[mentors["Ramy Farid"]][mentees["Leah Frye"]] = DISALLOWED

# Solve the Problem
cost_matrix = make_cost_matrix(matrix, lambda cost: (200 - cost) if (cost != DISALLOWED) else DISALLOWED)
m = Munkres()
indexes = m.compute(cost_matrix)


# Print the results
mentors = {v: k for k, v in mentors.items()}
mentees = {v: k for k, v in mentees.items()}
used_mentors = set()
used_mentees = set()
for row, column in indexes:
  value = matrix[row][column]
  mentor = mentors[row]
  mentee = mentees[column]
  print('(%s, %s) -> %d' % (mentor, mentee, value))
  used_mentors.add(mentor)
  used_mentees.add(mentee)

mentors = set([x for x in mentors.values()])
mentees = set([x for x in mentees.values()])
unused_mentees = mentees - used_mentees
unused_mentors = mentors - used_mentors
print("unused mentees: %s" % unused_mentees)
print("unused mentors: %s" % unused_mentors)
