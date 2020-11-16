import _hungarian
#from scipy.optimize import linear_sum_assignment as lsa
from numpy.random import rand
import numpy as np
#from itertools import product
import cProfile
#import pstats
#import io
#import matplotlib.pyplot as plt

# Setup
np.random.seed(161718)
cost_matrix = np.random.rand(300, 300)
sizes = [100, 300, 500, 700]
old_implementation_times = {}
new_implementation_times = {}



cProfile.run("_hungarian.linear_sum_assignment(cost_matrix)", sort="tottime")
# Loop over cases and extract times
"""for i, j in product(sizes, repeat=2):
    cost_matrix = rand(i, j)
    profile = cProfile.Profile()
    profile2 = cProfile.Profile()
    profile.enable()
    lsa(cost_matrix)
    profile.disable()
    s = io.StringIO()
    ps = pstats.Stats(profile, stream=s)
    ps.print_stats()
    out = float(s.getvalue().split('\n')[0].split(' ')[-2])
    old_implementation_times[(i, j)] = out


    profile2.enable()
    _hungarian.linear_sum_assignment(cost_matrix)
    profile2.disable()
    s = io.StringIO()
    ps = pstats.Stats(profile2, stream=s)
    ps.print_stats()
    out = float(s.getvalue().split('\n')[0].split(' ')[-2])
    new_implementation_times[(i, j)] = out


# Display times in chart
print(old_implementation_times, new_implementation_times)



labels = ['{}x{}'.format(int(i/100), int(j/100))
          for i, j in old_implementation_times.keys()]
print(labels)

ind = np.arange(len(sizes) ** 2) * 4  # the x locations for the groups
width = .35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, tuple(old_implementation_times.values()), width,
                color='SkyBlue', label='Old Implementation')
rects2 = ax.bar(ind + width/2, tuple(new_implementation_times.values()), width,
                color='IndianRed', label='New Implementation')

ax.set_ylabel('Times')
ax.set_title('Times given n x m random matrix (n, m in hundreds)')
ax.set_xticks(ind)
ax.set_xticklabels(labels)
ax.legend()

plt.show()
"""