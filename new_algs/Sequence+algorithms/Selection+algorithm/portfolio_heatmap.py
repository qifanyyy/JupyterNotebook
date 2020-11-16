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
sys.path.append("/Users/Chris/Documents/Summer-2014/arrow/arrow-space/FCCAuction/AuctionFiles/")
import mypyutils
from heatmapcluster import heatmapcluster
import numpy as np

#"CPU Time Used","Estimated Training Performance","Wallclock Time","Incumbent ID","Automatic Configurator (CPU) Time","Configuration..."

CPUHEADER = "CPU Time Used"
PERFORMANCEHEADER = "Estimated Training Performance"
 
def main(argv):

   try:
       opts, args = getopt.getopt(argv, "", ["file="])
   except getopt.GetoptError:
       raise NameError("Invalid arguments. Call string should look like:\nportfolio_heatmap.py --file <path-to-folder>")
   for opt, arg in opts:
       if opt in ("--file"):
           file = arg
       else:
           print ("Option " + opt + " is not recognized")
           print ("permutation_folds.py --data-file <path-to-file> --outputdir <path-to-output-dir> --seed_range <begin,end>")
           sys.exit(2)
   maxValue=10000  #Cutoff??
   with open(file, 'rU') as csvfile:
    lines = csv.DictReader(csvfile)
    values = []
    vbsValues = []
    for line in lines:
        row = []
        vbsRow = []
        minPerformance = 100000000
        bestSolver = ''     
        for col in line:
            if (float(line[col]) < minPerformance):
                minPerformance = float(line[col])
                bestSolver = col
            row.append(float(line[col]))
        for col in line:
            if col == bestSolver:
                vbsRow.append(line[bestSolver])
            else:
                vbsRow.append(maxValue)    
        vbsValues.append(vbsRow)    
        values.append(row)
   x_labels = list(xrange(len(values)))
   y_labels = list(xrange(len(values[0])))
   # Maybe you want to normalize each row???
   
   '''
   log_transform = False
   if log_transform:
       mypyutils.pyplot.plotHeatMap(values,x_labels, y_labels,colormap=plt.cm.get_cmap('RdBu'),norm=matplotlib.colors.LogNorm())
   else:
       mypyutils.pyplot.plotHeatMap(values,x_labels, y_labels,colormap=plt.cm.get_cmap('RdBu'))

   plt.xlabel("Hydra Iterations")
   plt.ylabel("Instances")
   plt.title("Hydra Portfolio Performance Heatmap")
   ax = plt.gca()
   cbar = plt.colorbar(orientation='vertical',pad=0.025,shrink=0.75,fraction=0.05)
   cbar.set_label('Performance', rotation=270,labelpad=15)
   cbar.ax.set_aspect(20)
   plt.show()
   
   plt.clf()
   log_transform = False
   if log_transform:
       mypyutils.pyplot.plotHeatMap(vbsValues,x_labels, y_labels,colormap=plt.cm.get_cmap('RdBu'),norm=matplotlib.colors.LogNorm())
   else:
       mypyutils.pyplot.plotHeatMap(vbsValues,x_labels, y_labels,colormap=plt.cm.get_cmap('RdBu'))
   plt.xlabel("Hydra Iterations")
   plt.ylabel("Instances")
   plt.title("Hydra Portfolio Performance Heatmap")
   ax = plt.gca()
   cbar = plt.colorbar(orientation='vertical',pad=0.025,shrink=0.75,fraction=0.05)
   cbar.set_label('Performance', rotation=270,labelpad=15)
   cbar.ax.set_aspect(20)
   '''
   np_values = np.array(values) 
   h = heatmapcluster(np_values, x_labels, y_labels,
                   num_row_clusters=3, num_col_clusters=0,
                   label_fontsize=6,
                   xlabel_rotation=-75,
                   cmap=plt.cm.coolwarm,
                   show_colorbar=True,
                   top_dendrogram=False)

   plt.show()
   '''
   print 'Saving Figure...'
   plt.savefig('/Users/Chris/Desktop/boxplot_matlab_java_comparison.png', bbox_inches='tight', dpi=100)
   plt.show()  
   '''   

if __name__ == "__main__":
    main(sys.argv[1:])
