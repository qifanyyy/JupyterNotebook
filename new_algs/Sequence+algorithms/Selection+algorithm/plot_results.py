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


  iterations = [0,1,2,3,4,5,6,7]
  base_results_miphydra = [6.854519999999999,1.1834,0.66264,0.60308,0.50556,0.49420000000000003,0.44156,0.41567999999999994]
  improved_results_miphydra = [4.959040000000001,1.8708400000000003,0.985,0.7326800000000001,0.6738,0.56416,0.467559999999999,0.4214]
  base_results = [20.896639999999998,14.614320000000001,10.67228,7.9658,5.95936,5.95544,5.12924,4.51328]
  improved_results = [17.06872,11.299999999999999,8.47456,5.10336,3.4604399999999997,3.24212,2.39288,2.19604]
  fig=plt.figure()
  axis = fig.add_subplot(111)  
  plt.plot(iterations, base_results_miphydra, label = "HydraMIP-WS-Marginal-ChallengerSelect")
  plt.plot(iterations, improved_results_miphydra, label = "HydraMIP-baseline")
  plt.plot(iterations, base_results, label = "Original-Baseline")
  plt.plot(iterations, improved_results , label = "Original-WS-Marginal-ChallengerSelect")

  plt.ylabel('Performance (Mean PAR10)')
  plt.xlabel('Iterations')
  plt.title('Hydra Performance')
  plt.yscale('log')
  plt.legend()
    
  plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])