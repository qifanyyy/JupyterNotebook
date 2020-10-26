# Main file

# Python implementation

# A cortical sparse distributed coding model linking mini- and
# macrocolumn-scale functionality - Gerard J. Rinkus (doi: 10.3389/fnana.2010.00017)
# FIGURE 2 | Functional architecture

# Aakanksha Mathuria
# Portland State University

import numpy as np
from Macrocolumn_Func1 import Macrocolumn_Func1
from Hebbs import Hebbs

i = 3
j = 12
q = 4

Hebb = Hebbs()
Macrocolumn = Macrocolumn_Func1()

IN = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
IN0 = [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0]

overlap = np.dot(IN, IN0)

f = np.zeros([q, i])
W = Hebb.Hebbs_cr(IN, IN0, f)
F2 = Macrocolumn.Macrocolumn_Func1_cr(IN0, 1, W, overlap)
print("F2 ", F2)

# first iteration
IN1 = [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0]

# Calculate overlap of IN0 and IN1
overlap = np.dot(IN0, IN1)
print("Overlap ", overlap)

Wc1 = Hebb.Hebbs_cr(IN0, IN1, F2)
F2i1 = Macrocolumn.Macrocolumn_Func1_cr(IN1, 2, Wc1, overlap)
print("F2i1 ", F2i1)

# second iteration
IN2 = [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1]

# Calculate overlap of IN1 and IN2
overlap = np.dot(IN0, IN2)
print("Overlap ", overlap)

Wc2 = Hebb.Hebbs_cr(IN0, IN2, F2)
F2i2 = Macrocolumn.Macrocolumn_Func1_cr(IN2, 2, Wc2, overlap)
print("F2i2 ", F2i2)

# Third iteration
IN3 = [0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1]

# Calculate overlap of IN1 and IN2
overlap = np.dot(IN0, IN3)
print("Overlap", overlap)

Wc3 = Hebb.Hebbs_cr(IN0, IN3, F2)
F2i3 = Macrocolumn.Macrocolumn_Func1_cr(IN3, 3, Wc3, overlap)
print("F2i3 ", F2i3)

# fourth iteration
IN4 = [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1]

# Calculate overlap of IN1 and IN2
overlap = np.dot(IN0, IN4)
print("Overlap", overlap)

Wc4 = Hebb.Hebbs_cr(IN0, IN4, F2)
F2i4 = Macrocolumn.Macrocolumn_Func1_cr(IN4, 3, Wc4, overlap)
print("F2i4 ", F2i4)