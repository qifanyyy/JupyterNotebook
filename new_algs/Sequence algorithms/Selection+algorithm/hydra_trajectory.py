''' 
This script takes a hydra output folder and produces a plot of hydra performance trajectory
 @author Chris Cameron
 '''
 
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import sys
import csv
from itertools import cycle
import getopt
import os

#"CPU Time Used","Estimated Training Performance","Wallclock Time","Incumbent ID","Automatic Configurator (CPU) Time","Configuration..."

CPUHEADER = "CPU Time Used"
PERFORMANCEHEADER = "Estimated Training Performance"

'''Get all trajectory files from hydra iteration '''
def getTrajectoryFilesForIteration(iteration, directory):
    
    trajFiles = []
    
    subdirs = [x[0] for x in os.walk(directory)]                                                                            
    for subdir in subdirs:
        if "Iteration_" + str(iteration) in subdir:
            files = os.walk(subdir).next()[2]
            for file in files:
                if "detailed-traj" in file:
                    trajFiles.append(os.path.join(os.path.join(directory,subdir),file))                                                                             
    
    return trajFiles
    
def getPerformanceTrajectory(trajFile, cpuTime):
    
    cpu_times = []
    performances = []
    first = True
    
    with open(trajFile, 'rU') as csvfile:
        lines = csv.DictReader(csvfile)
        
        for line in lines:
            #print cpuTime
            if not first:
                cpu_times.append(float(line[CPUHEADER]) + cpuTime)
                # May want to subtract from VBS performance in previous iteration??
                performances.append(float(line[PERFORMANCEHEADER]))
            else:    
                first = False
    
    return (cpu_times, performances)
    
 
def main(argv):

   try:
       opts, args = getopt.getopt(argv, "", ["hydra-directory=", "output-file="])
   except getopt.GetoptError:
       raise NameError("Invalid arguments. Call string should look like:\nhydra_trajectory.py --hydra-directory <path-to-folder> --output-file <output_file>")
   for opt, arg in opts:
       if opt in ("--hydra-directory"):
           hydraDirectory = arg
       elif opt in ("--output-file"):
           filename = arg 
       else:
           print "Option " + opt + " is not recognized"
           print "permutation_folds.py --data-file <path-to-file> --outputdir <path-to-output-dir> --seed_range <begin,end>"
           sys.exit(2)

   print "Plotting hydra trajectory from results directory: " + hydraDirectory
   smacRunsDirectory = os.path.join(hydraDirectory, "smac_runs")
   
   if not os.path.isdir(smacRunsDirectory):
       raise Exception('Provided hydra folder %s does not contains smac_runs folder! smac information cannot be found.' % hydraDirectory)

   smac_runs = []
   hydra_iteration = 0
   cpuTime = 0
   maxCPUTime = 0
   
   while(True):
       print "Parsing for hydra iteration: " + str(hydra_iteration)
       trajFiles = getTrajectoryFilesForIteration(hydra_iteration, smacRunsDirectory)
       if trajFiles == []:
           break
       for trajFile in trajFiles:
           smac_run = getPerformanceTrajectory(trajFile, cpuTime)
           smac_run_max_cpu_time = max(smac_run[0])
           smac_runs.append(smac_run)
           if smac_run_max_cpu_time > maxCPUTime:
               maxCPUTime = smac_run_max_cpu_time
       #Update cumulative CPU time
       cpuTime = maxCPUTime
       
       hydra_iteration += 1
   
       #fig=plt.figure(1,figsize=(fig_height,fig_width))

   fig=plt.figure()
   axis = fig.add_subplot(111)      
   colors = ['g','y','r','k','b']
   color_cycler = cycle(colors)

   plt.ylabel("Incumbent Performance")
   plt.xlabel('CPU time (s)')
   plt.title('Trajectory: ' +  hydraDirectory)
     
   for smac_run in smac_runs:
       
       cpu_times = smac_run[0]
       performances = smac_run[1]
       #print cpu_times
       #print performances
       #lines.Line2D(cpu_times,performances,color=color_cycler.next())
       axis.plot(cpu_times,performances,color=color_cycler.next())

   axis.set_yscale('log')
   axis.set_ylim(bottom=0.01)
   print 'Saving Figure...'
   #plt.savefig('/Users/Chris/Desktop/plots/hydra/' + filename, bbox_inches='tight', dpi=100)
   plt.show()  
      

if __name__ == "__main__":
    main(sys.argv[1:])