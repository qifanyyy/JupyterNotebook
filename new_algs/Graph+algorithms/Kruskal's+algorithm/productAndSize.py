# Purpose: Conduct an experiment to prove that the product of two numbers
# does not depend on the size of the two numbers being multiplied. Write a program
# that plots the results of multiplying numbers of various sizes together. HINT:
# To get a good reading you may want to do more than one of these multiplications and
# time them as a group since a multiplication happens pretty quickly in a computer.
# Verify that it truly is a O(1) operation. Do you see any anomalies? It might be
# explained by Python's support of large integers. What is the cutoff point for handling
# multiplications in constant time? Why? Write a program that produces an XML file with
# your results in the format given in this chapter. Then visualize your results with the
# PlotData.py program provided in this chapter.
# Date: 9/5/18
# @author: Katie Hummel

# Q: What do you see?
# A: The graph appears to slope up, then down, then up and down again always 
# hovering just around 1 millisecond, until the length of the number being 
# multiplied is 6; here the computation time jumps to 9 milliseconds before 
# resuming the normal 1 millisecond time. The same ordeal occurs when x = 7 where
# the time to multiply the two numbers skyrocketed to 18 milliseconds for a couple
# of the data points.
#
# Q: Do you see any anomalies?
# A: As mentioned above, there are two spikes in the graph where the length of 
# the number being multiplied against itself where abnormally high compared to the 
# rest of plot points--where the length was 6 and 7. For these particular x values
# the computation time was quite large. However, this abnormality did not occurer 
# for every x value with a length of 6 or 7, just a select few.
#
# Q: What is the cutoff point for handling multiplications in constant time? Why?
# A: From what I've gathered from my graph, the cutoff point for handling 
# multiplications in constant time may be at 1,0000,000,000 (where length is 6)
# as that was where the computation time spiked up and appears to do so very 
# every power of 10 thereafter. This may be because of the way Python handles
# very large numbers. 

# Note: this program will take about 10 seconds to run

import datetime
import random


def main():
    # Write an XML file with the results
    file = open("results.xml", "w")

    # File version and title
    file.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
    file.write('<Plot title="Computation Time of the Product of Two Numbers">\n')

    # File Axes
    file.write('  <Axes>\n')
    file.write('    <XAxis min="' + str(0) + '" max="' + str(8) + '">Length of a Number to be Multiplied with Itself</XAxis>\n')
    file.write('    <YAxis min="' + str(0) + '" max="' + str(30) + '">Milliseconds</YAxis>\n')
    file.write('  </Axes>\n')

    # (product, time)
    numLen = []
    time = [] 
    for i in range(0, 10000000):
        if i%50 == 0:
            numLen.append(len(str(i)))
            starttime = datetime.datetime.now()
            for j in range(1000):
                prod = i*i
            endtime = datetime.datetime.now()

            deltaT = (endtime - starttime)
            deltaTMicrosec = deltaT.microseconds
            deltaTMillisec = deltaTMicrosec * 1E-3
            
            time.append(deltaTMillisec)

    file.write('  <Sequence title="Time Versus the Product of Two Numbers" color="blue">\n')
    for i in range(len(numLen)):
        file.write('    <DataPoint x="' + str(numLen[i]) + '" y="' + str(time[i]) + '"/>\n')
    file.write('  </Sequence>\n')

    file.write('</Plot>\n')
    file.close()

    print("Program completed.")


if __name__ == "__main__":
    main()
