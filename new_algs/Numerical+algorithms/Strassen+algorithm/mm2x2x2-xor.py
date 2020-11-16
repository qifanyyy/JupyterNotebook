# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 19:31:50 2014

@author: Eugene Petkevich
"""

import satmaker

# To make an input for a SAT-solver, we need to associate each variable with
# a number automatically, while keeping string reference for ourselves.
# For this we use a VariableFactory and ConstraintCollector classes.

vf = satmaker.VariableFactory();
cc = satmaker.ConstraintCollector();

# Here we define constants: size and numbers of multiplication vectors.

MATRIX_SIZE = 2
MULTIPLICATION_VECTORS = 15

# We start with basic variables, 24 variables for each of the 15
# final computed multiplications:  8 for each of elements of first matrix (A),
# 4 for second matrix (B), and 4 for third matrix(C).

a = [[[[vf.next()
        for la in range(MATRIX_SIZE)]
       for ja in range(MATRIX_SIZE)]
      for ia in range(MATRIX_SIZE)]
     for k in range(MULTIPLICATION_VECTORS)]
b = [[[[vf.next()
        for lb in range(MATRIX_SIZE)]
       for jb in range(MATRIX_SIZE)]
      for ib in range(MATRIX_SIZE)]
     for k in range(MULTIPLICATION_VECTORS)]
c = [[[[vf.next()
        for lc in range(MATRIX_SIZE)]
       for jc in range(MATRIX_SIZE)]
      for ic in range(MATRIX_SIZE)]
     for k in range(MULTIPLICATION_VECTORS)]

# Now we calculate result vectors of the product matrix D (D = A*B*C).

d = []
for id in range(MATRIX_SIZE):
    d.append([])
    for jd in range(MATRIX_SIZE):
        d[id].append([])
        for ld in range(MATRIX_SIZE):
            d[id][jd].append([])
            for ia in range(MATRIX_SIZE):
                d[id][jd][ld].append([])
                for ja in range(MATRIX_SIZE):
                    d[id][jd][ld][ia].append([])
                    for la in range(MATRIX_SIZE):
                        d[id][jd][ld][ia][ja].append([])
                        for ib in range(MATRIX_SIZE):
                            d[id][jd][ld][ia][ja][la].append([])
                            for jb in range(MATRIX_SIZE):
                                d[id][jd][ld][ia][ja][la][ib].append([])
                                for lb in range(MATRIX_SIZE):
                                    d[id][jd][ld][ia][ja][la][ib][jb].append([])
                                    for ic in range(MATRIX_SIZE):
                                        d[id][jd][ld][ia][ja][la][ib][jb][lb].append([])
                                        for jc in range(MATRIX_SIZE):
                                            d[id][jd][ld][ia][ja][la][ib][jb][lb][ic].append([])
                                            for lc in range(MATRIX_SIZE):
                                                d[id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc].append(False)

for id in range(MATRIX_SIZE):
    for jd in range(MATRIX_SIZE):
        for ld in range(MATRIX_SIZE):
            for o in range(MATRIX_SIZE):
                d[id][jd][ld][id][jd][o][id][o][ld][o][jd][ld] = True

# Now we define coefficients q_k_id_jd_ld, k in 1..15, {id, jd, ld} in 1..2,
# for linking multiplication and result vectors:
# <xor for all k in 1..15> m_k_ia_ja_la_ib_jb_lb_ic_jc_lc and q_k_id_jd_ld = d_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc
# for {id, jd, ld, ia, ja, la, ib, jb, lb, ic, jc, lc} in 1..2.

q = [[[[vf.next()
        for ld in range(MATRIX_SIZE)]
       for jd in range(MATRIX_SIZE)]
      for id in range(MATRIX_SIZE)]
     for k in range(MULTIPLICATION_VECTORS)]

# Now we define second series of constraints,
# that link multiplication vectors and result vectors.
# We rewrite previous constraints as a step by step computation,
# with introducing additional variables p_k_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc and t_k_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc,
# such that:
# p_k_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc = m_k_ia_ja_la_ib_jb_lb_ic_jc_lc and q_k_id_jd_ld,
# k in 1..15, {id, jd, ld, ia, ja, la, ib, jb, lb, ic, jc, lc} in 1..2;
# and
# t_k_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc = t_(k-1)_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc xor p_k_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc,
# k in 2..15, {id, jd, ld, ia, ja, la, ib, jb, lb, ic, jc, lc} in 1..2,
# t_1_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc = p_1_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc;
# and
# t_15_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc = d_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc,
# {id, jd, ld, ia, ja, la, ib, jb, lb, ic, jc, lc} in 1..2;
# The last one is rewritten as
# t_15_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc or not(t_15_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc),
# depending on d_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc value, which is known by definition.

# So we define variables p and constraints for them:

p = [[[[[[[[[[[[[vf.next()
                 for lc in range(MATRIX_SIZE)]
                for jc in range(MATRIX_SIZE)]
               for ic in range(MATRIX_SIZE)]
              for lb in range(MATRIX_SIZE)]
             for jb in range(MATRIX_SIZE)]
            for ib in range(MATRIX_SIZE)]
           for la in range(MATRIX_SIZE)]
          for ja in range(MATRIX_SIZE)]
         for ia in range(MATRIX_SIZE)]
        for ld in range(MATRIX_SIZE)]
       for jd in range(MATRIX_SIZE)]
      for id in range(MATRIX_SIZE)]
     for k in range(MULTIPLICATION_VECTORS)]

for k in range(MULTIPLICATION_VECTORS):
    for id in range(MATRIX_SIZE):
        for jd in range(MATRIX_SIZE):
            for ld in range(MATRIX_SIZE):
                for ia in range(MATRIX_SIZE):
                    for ja in range(MATRIX_SIZE):
                        for la in range(MATRIX_SIZE):
                            for ib in range(MATRIX_SIZE):
                                for jb in range(MATRIX_SIZE):
                                    for lb in range(MATRIX_SIZE):
                                        for ic in range(MATRIX_SIZE):
                                            for jc in range(MATRIX_SIZE):
                                                for lc in range(MATRIX_SIZE):
                                                    va = a[k][ia][ja][la]
                                                    vb = b[k][ib][jb][lb]
                                                    vc = c[k][ic][jc][lc]
                                                    vd = q[k][id][jd][ld]
                                                    ve = p[k][id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc][lc]
                                                    cc.add(positive=[ve],
                                                           negative=[va, vb, vc, vd])
                                                    cc.add(positive=[va],
                                                           negative=[ve])
                                                    cc.add(positive=[vb],
                                                           negative=[ve])
                                                    cc.add(positive=[vc],
                                                           negative=[ve])
                                                    cc.add(positive=[vd],
                                                           negative=[ve])

# So we define variables t and constraints for them. First, a transformation:
# c = a xor b
# can be rewritten as
# c = (a or b) and (not(a) or not(b))
# which in turn is
# (c or not((a or b)) or not((not(a) or not(b)))) and (not(c) or (a or b)) and (not(c) or (not(a) or not(b)))
# which is equal to
# (c or (not(a) and not(b)) or (a and b)) and (not(c) or a or b) and (not(c) or not(a) or not(b))
# which is equal to
# (c or not(a) or b) and (c or a or not(b)) and (not(c) or a or b) and (not(c) or not(a) or not(b))
# This is correct, Tseitin transformations

t = [[[[[[[[[[[[vf.next()
                for lc in range(MATRIX_SIZE)]
               for jc in range(MATRIX_SIZE)]
              for ic in range(MATRIX_SIZE)]
             for lb in range(MATRIX_SIZE)]
            for jb in range(MATRIX_SIZE)]
           for ib in range(MATRIX_SIZE)]
          for la in range(MATRIX_SIZE)]
         for ja in range(MATRIX_SIZE)]
        for ia in range(MATRIX_SIZE)]
       for ld in range(MATRIX_SIZE)]
      for jd in range(MATRIX_SIZE)]
     for id in range(MATRIX_SIZE)]

for id in range(MATRIX_SIZE):
    for jd in range(MATRIX_SIZE):
        for ld in range(MATRIX_SIZE):
            for ia in range(MATRIX_SIZE):
                for ja in range(MATRIX_SIZE):
                    for la in range(MATRIX_SIZE):
                        for ib in range(MATRIX_SIZE):
                            for jb in range(MATRIX_SIZE):
                                for lb in range(MATRIX_SIZE):
                                    for ic in range(MATRIX_SIZE):
                                        for jc in range(MATRIX_SIZE):
                                            for lc in range(MATRIX_SIZE):
                                                positive = []
                                                negative = []
                                                for k in range(MULTIPLICATION_VECTORS-1):
                                                    positive.append(p[k][id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc][lc])
                                                k = MULTIPLICATION_VECTORS-1
                                                if d[id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc][lc]:
                                                    positive.append(p[k][id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc][lc])
                                                else:
                                                    negative.append(p[k][id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc][lc])
                                                cc.add_xor(positive=positive,
                                                           negative=negative)

# We have in the end 66016 variables, 311296 clauses, 860160 literals.

# Now we will output all the constraints to a file that will be an input to
# a SAT solver.
# For printing we will use a SatPrinter class.

sp = satmaker.SatPrinter(vf, cc);
sp.print_statistics()
file = open('input-2x2x2-xor.txt', 'wt')
sp.print(file)
file.close()
'''
# Now a SAT solver should be executed and store its output in output.txt file.
# We get back data from the output to variables.

file = open('output.txt', 'rt')
sp.decode_output(file)
file.close()

# We print the important variables into a text file in easily readable form.

file = open('solution.txt', 'wt')
for k in range(7):
    file.write('M_' + str(k+1) + ' = (')
    members = []
    for ia in range(2):
        for ja in range(2):
            if (a[k][ia][ja]['value']):
                members.append('A' + str(ia+1) + '' + str(ja+1))
    file.write(' + '.join(members) + ')(')
    members = []
    for ib in range(2):
        for jb in range(2):
            if (b[k][ib][jb]['value']):
                members.append('B' + str(ib+1) + '' + str(jb+1))
    file.write(' + '.join(members) + ')\n')
for ic in range(2):
    for jc in range(2):
        file.write('C' + str(ic+1) + str(jc+1) + ' = ')
        members = []
        for k in range(7):
            if q[k][ic][jc]['value']:
                members.append('M' + str(k+1))
        file.write(' + '.join(members) + '\n')
file.close()
'''
