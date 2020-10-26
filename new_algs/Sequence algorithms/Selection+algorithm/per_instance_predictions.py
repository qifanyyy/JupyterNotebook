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
from scipy import stats
sys.path.append("/Users/Chris/Documents/Summer-2014/arrow/arrow-space/FCCAuction/AuctionFiles/")
import mypyutils


#"CPU Time Used","Estimated Training Performance","Wallclock Time","Incumbent ID","Automatic Configurator (CPU) Time","Configuration..."

PERFORMANCEHEADER = "performance"
PREDICTEDPERFORMANCEHEADER = "predictedPerformance"
CPUTIMEHEADER = "CPUtime"
CONFIGID = "ConfigID"
run = "RUNID"

CHALLENGEREXPECTEDBETTER="ChallengerExpectedBetter"
 
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
 
  # Get directory and get state-run/challenger-predictions file from there
   challengerInstancePerformances = {}
   challengerExpectedBetter = {}
   realPerformances = []
   predictedPerformances = []
   CUTOFF = 5
   with open(file, 'rU') as csvfile:
       lines = csv.DictReader(csvfile)
       x_data = []
       y_data = []
       for line in lines:
           realPerformance = float(line[PERFORMANCEHEADER])
           if realPerformance >= CUTOFF:
               print realPerformance >= CUTOFF
               print realPerformance
               realPerformance = CUTOFF*10
           predictedPerformance = line[PREDICTEDPERFORMANCEHEADER]
           realPerformances.append(realPerformance)
           predictedPerformances.append(predictedPerformance)
           
           
           y_data.append(str(100 * (float(predictedPerformance) - float(realPerformance)) / (float(realPerformance)+0.01)))
           x_data.append(line[CPUTIMEHEADER])
           
           if not line[CONFIGID] in challengerInstancePerformances.keys():
               challengerInstancePerformances[line[CONFIGID]] = []
           a = challengerInstancePerformances[line[CONFIGID]]
           a.append(float(realPerformance))
           challengerInstancePerformances[line[CONFIGID]] = a
           
           challengerExpectedBetter[line[CONFIGID]] = line[CHALLENGEREXPECTEDBETTER] == 'true'
           


       #stats.spearmanr(a,b)    
           
           # See if ordering is correct
   #print challengerInstancePerformances
   spearman_coefficients = []
   data = []
   for challenger in challengerInstancePerformances:
       num_runs = len(challengerInstancePerformances[challenger])
       performances = challengerInstancePerformances[challenger]
       data.append(num_runs)
       #print performances
       indices = list(xrange(num_runs))
       sortedIndices = [i[0] for i in sorted(enumerate(performances), key=lambda x:x[1])]
       #print indices
       r = stats.spearmanr(indices,sortedIndices)

       if not len(indices) == 1 and challengerExpectedBetter[challenger]:
            #print r[0]
            #print indices 
            #print sortedIndices
            
            # Only if challenger expeted better
            spearman_coefficients.append(r[0])
   
   '''
   print spearman_coefficients
   mypyutils.pyplot.plotECDF(spearman_coefficients,color='g',linewidth=1.0,linestyle='None',label=None)
   plt.show()
   mypyutils.pyplot.customboxplot(spearman_coefficients,mean=True)
   plt.show()
   #print data
   mypyutils.pyplot.plotECDF(data,color='g',linewidth=1.0,linestyle='None',label=None)
   plt.xlabel('Num Challenger Runs')
   plt.title('ECDF of Number of runs per challenger')
   '''
           
   '''
   fig=plt.figure()
   axis = fig.add_subplot(111)  
   plt.plot(x_data, y_data, linestyle='', marker = "o")

   axis.set_ylim([-100,100])
   plt.ylabel("Prediction Error (%)")
   plt.xlabel('CPU time (s)')
   plt.title('Per instance prediction error')
   '''
   fig=plt.figure()
   axis = fig.add_subplot(111)  
   plt.plot(realPerformances, predictedPerformances, linestyle='', marker = "o")  
   #axis.set_xlim([0,5])
   #axis.set_ylim([0,5])
    
   
   plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])