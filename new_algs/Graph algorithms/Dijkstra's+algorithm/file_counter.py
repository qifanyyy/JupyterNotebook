import os
import time
import sys


def num_files(directory):
    i = 0
    for f in directory:
        i += 1

    return i


input_directory = raw_input("Enter the input directory: ")
data_directory = raw_input("Enter the data directory: ")

start = time.time()
target_num = num_files(os.listdir(input_directory))


print "Number of files in " + input_directory + " is: " + str(target_num) + '\n'

while True:
    data_num = num_files(os.listdir(data_directory))
    perc = float(data_num)/float(target_num)
    end = time.time()
    print "{0:30}{1:>10}{2:>15}".format("Number of files: " + str(data_num), str(100 * perc) + ' %', 'Time: ' + str(round(end - start, 2)))
    #print "Number of files in " + data_directory + " is: " + str(data_num)
    

    if data_num == target_num:
        print "-----Done-----"
        sys.exit()

    time.sleep(1)
    sys.stdout.write("\033[F") # Cursor up one line





