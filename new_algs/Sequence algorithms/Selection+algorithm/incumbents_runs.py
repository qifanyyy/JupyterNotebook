''' 
This script takes a hydra output folder and produces a plot of hydra performance trajectory
 @author Chris Cameron
 '''
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import sys
import csv
from itertools import cycle
import getopt
import os
#"CPU Time Used","Estimated Training Performance","Wallclock Time","Incumbent ID","Automatic Configurator (CPU) Time","Configuration..."

INCUMBENTRUNSEHEADER = "Incumbent Runs"
CPUTIMEHEADER = "CPUtime"

 
def main(argv):

   try:
       opts, args = getopt.getopt(argv, "", ["file="])
   except getopt.GetoptError:
       raise NameError("Invalid arguments. Call string should look like:\nportfolio_heatmap.py --file <path-to-folder>")
   for opt, arg in opts:
       if opt in ("--file"):
           file = arg
       else:
           print "Option " + opt + " is not recognized"
           print "permutation_folds.py --data-file <path-to-file> --outputdir <path-to-output-dir> --seed_range <begin,end>"
           sys.exit(2)

   with open(file, 'rU') as csvfile:
    lines = csv.DictReader(csvfile)
    x_data = []
    y_data = []
    for line in lines:
        x_data.append(line[CPUTIMEHEADER])
        y_data.append(line[INCUMBENTRUNSEHEADER])

   
   fig=plt.figure()
   axis = fig.add_subplot(111)  
   plt.plot(x_data, y_data)

   plt.ylabel('Num Incumbent Runs')
   plt.xlabel('CPU time (s)')
   plt.title('Incumbent Progress')

   plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])