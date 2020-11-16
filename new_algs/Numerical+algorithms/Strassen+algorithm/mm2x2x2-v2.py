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

# For each multiplication vector m_k we define a variable
# for each combination of a, b and c variables
# that correspond to value of their product (exists or not in m_k).

m = [[[[[[[[[[vf.next()
              for lc in range(MATRIX_SIZE)]
             for jc in range(MATRIX_SIZE)]
            for ic in range(MATRIX_SIZE)]
           for lb in range(MATRIX_SIZE)]
          for jb in range(MATRIX_SIZE)]
         for ib in range(MATRIX_SIZE)]
        for la in range(MATRIX_SIZE)]
       for ja in range(MATRIX_SIZE)]
      for ia in range(MATRIX_SIZE)]
     for k in range(MULTIPLICATION_VECTORS)]

# Now we define first series of constraints,
# that link basic variables and multiplication vectors.
# For each k in 1..15, {ia, ja, la, ib, jb, lb, ic, jc, lc} in 1..2:
# m_k_ia_ja_la_ib_jb_lb_ic_jc_lc = a_k_ia_ja_la and b_k_ib_jb_lb and c_k_ic_jc_lc
# or in short:  d = a and b and c
# which can be rewritten as
# (d or ~a or ~b or ~c) and (~d or a) and (~d or b) and (~d or c).

for k in range(MULTIPLICATION_VECTORS):
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
                                        vd = m[k][ia][ja][la][ib][jb][lb][ic][jc][lc]
                                        cc.add(positive=[vd],
                                               negative=[va, vb, vc])
                                        cc.add(positive=[va],
                                               negative=[vd])
                                        cc.add(positive=[vb],
                                               negative=[vd])
                                        cc.add(positive=[vc],
                                               negative=[vd])

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
# However, we don't introduce p variables in code, and instead use a transformation:
# d = (a and e) xor (b and c)
# is equivalent to
# (~a | ~e | ~b | ~c | ~d) ∧ (a ∨ b ∨ ~d) ∧ (e ∨ b ∨ ~d) ∧ (a ∨ c ∨ ~d) ∧ (e ∨ c ∨ ~d) ∧ (a ∨ ~b | ~c ∨ d) ∧ (e ∨ ~b | ~c ∨ d) ∧ (~a | ~e ∨ b ∨ d) ∧ (~a | ~e ∨ c ∨ d).
# And a transformation:
# d = a xor (b and c)
# is equivalent to
# (~a | ~b | ~c | ~d) ∧ (a ∨ b ∨ ~d) ∧ (a ∨ c ∨ ~d) ∧ (a ∨ ~b | ~c ∨ d) ∧ (~a ∨ b ∨ d) ∧ (~a ∨ c ∨ d).

t = [[[[[[[[[[[[[vf.next()
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
     for k in range(MULTIPLICATION_VECTORS-1)]

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
                                                va = m[0][ia][ja][la][ib][jb][lb][ic][jc][lc]
                                                ve = q[0][id][jd][ld]
                                                vb = m[1][ia][ja][la][ib][jb][lb][ic][jc][lc]
                                                vc = q[1][id][jd][ld]
                                                vd = t[0][id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc][lc]
                                                cc.add(positive=[],
                                                       negative=[va, ve, vb, vc, vd])
                                                cc.add(positive=[va, vb],
                                                       negative=[vd])
                                                cc.add(positive=[va, vc],
                                                       negative=[vd])
                                                cc.add(positive=[ve, vb],
                                                       negative=[vd])
                                                cc.add(positive=[ve, vc],
                                                       negative=[vd])
                                                cc.add(positive=[va, vd],
                                                       negative=[vb, vc])
                                                cc.add(positive=[ve, vd],
                                                       negative=[vb, vc])
                                                cc.add(positive=[vb, vd],
                                                       negative=[va, ve])
                                                cc.add(positive=[vc, vd],
                                                       negative=[va, ve])

for k in range(1, MULTIPLICATION_VECTORS-1):
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
                                                    va = t[k-1][id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc][lc]
                                                    vb = m[k+1][ia][ja][la][ib][jb][lb][ic][jc][lc]
                                                    vc = q[k+1][id][jd][ld]
                                                    vd = t[k][id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc][lc]
                                                    cc.add(positive=[],
                                                           negative=[va, vb, vc, vd])
                                                    cc.add(positive=[va, vb],
                                                           negative=[vd])
                                                    cc.add(positive=[va, vc],
                                                           negative=[vd])
                                                    cc.add(positive=[va, vd],
                                                           negative=[vb, vc])
                                                    cc.add(positive=[vb, vd],
                                                           negative=[va])
                                                    cc.add(positive=[vc, vd],
                                                           negative=[va])

# And last constraints:
# t_14_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc = c_id_jd_ld_ia_ja_la_ib_jb_lb_ic_jc_lc,
# {id, jd, ld, ia, ja, la, ib, jb, lb, ic, jc, lc} in 1..2.

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
                                                if d[id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc][lc]:
                                                    cc.add(positive=[t[MULTIPLICATION_VECTORS-2][id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc][lc]], negative=[])
                                                else:
                                                    cc.add(positive=[], negative=[t[MULTIPLICATION_VECTORS-2][id][jd][ld][ia][ja][la][ib][jb][lb][ic][jc][lc]])

# We have in the end 65504 variables, 391168 clauses, 1281024 literals.

# Now we will output all the constraints to a file that will be an input to
# a SAT solver.
# For printing we will use a SatPrinter class.

sp = satmaker.SatPrinter(vf, cc);
file = open('input-2x2x2-v2.txt', 'wt')
sp.print(file)
file.close()

# Now a SAT solver should be executed and store its output in output.txt file.
# We get back data from the output to variables.
'''
file = open('output-3d.txt', 'rt')
sp.decode_output(file)
file.close()

# We print the important variables into a text file in easily readable form.

file = open('solution-3d.txt', 'wt')
for k in range(MULTIPLICATION_VECTORS):
    file.write('M_' + str(k+1) + ' = (')
    members = []
    for ia in range(MATRIX_SIZE):
        for ja in range(MATRIX_SIZE):
            for la in range(MATRIX_SIZE):
                if (a[k][ia][ja][la]['value']):
                    members.append('A' + str(ia+1) + '' + str(ja+1) + '' + str(la+1))
    file.write(' + '.join(members) + ')(')
    members = []
    for ib in range(MATRIX_SIZE):
        for jb in range(MATRIX_SIZE):
            for lb in range(MATRIX_SIZE):
                if (b[k][ib][jb][lb]['value']):
                    members.append('B' + str(ib+1) + '' + str(jb+1) + '' + str(lb+1))
    file.write(' + '.join(members) + ')(')
    members = []
    for ic in range(MATRIX_SIZE):
        for jc in range(MATRIX_SIZE):
            for lc in range(MATRIX_SIZE):
                if (c[k][ic][jc][lc]['value']):
                    members.append('C' + str(ic+1) + '' + str(jc+1) + '' + str(lc+1))
    file.write(' + '.join(members) + ')\n')
for id in range(MATRIX_SIZE):
    for jd in range(MATRIX_SIZE):
        for ld in range(MATRIX_SIZE):
            file.write('D' + str(id+1) + str(jd+1) + str(ld+1) + ' = ')
            members = []
            for k in range(MULTIPLICATION_VECTORS):
                if q[k][id][jd][ld]['value']:
                    members.append('M' + str(k+1))
            file.write(' + '.join(members) + '\n')
file.close()
'''
