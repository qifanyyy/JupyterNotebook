#!/usr/bin/python
import csv
import re
import sys

teams={}
map={}
count=0
winSparse={}
losses={}
if len(sys.argv)>1: teamprint=1
else: teamprint=0

with open('scores.csv','rb') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    for row in csv_reader:
        ### remove rankings, create map of teams/integer ###
 	win = re.sub("^\(.*\) ", "",row[5])
        lose = re.sub("^\(.*\) ", "",row[8])
       
        if win not in teams:
	 teams[win]=count
	 map[count]=win
	 losses[count]=0
	 count+=1
        if lose not in teams:
	 teams[lose]=count
	 map[count]=lose
	 losses[count]=0
	 count+=1

   
        value = 1
        #### extra point for a blowout ###
        #if int(row[6])-int(row[9])>10: value+=0.5
        #### extra point for a win on the road ###
        #if row[7]=="@": value+=0.5
       
        ### create sparse matrix for each loser - increment number of wins ###
        if teams[lose] not in winSparse: 
	    winSparse[teams[lose]]={} 
	    #winSparse[teams[lose]][teams[lose]]=1
        if teams[win] not in winSparse[teams[lose]]: winSparse[teams[lose]][teams[win]]=0
        winSparse[teams[lose]][teams[win]]+=value
        losses[teams[lose]]+=value 

#### print team mapping to file ####
if teamprint==1:
 for i in range(0,len(teams)):
  print "%d,%s" % (i,map[i])

### print out H matrix ###
if teamprint!=1:
 for i in range(0,len(teams)):
  for j in range(0,len(teams)):
     if i not in winSparse: winSparse[i]={}
     #if j in winSparse[i]: print "%f" % (winSparse[i][j]/float(losses[i])),
     if j in winSparse[i]: print "%f" % (float(winSparse[i][j])/max(13,losses[i])),
     else: print 0,
  print
