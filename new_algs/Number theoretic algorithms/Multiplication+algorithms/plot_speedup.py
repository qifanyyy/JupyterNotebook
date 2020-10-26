#!/usr/bin/python
import sys
import matplotlib.pyplot as plt
import os

def plot_speed_up(dir):
    T_serial = -1.0
    p_list = [1, 4, 9, 16, 25, 36]
    time_list = []

    i = 0
    for P in p_list:
        name = "time_"+str(P)+".txt"
        filename = os.path.join(dir,name)
        f = open(filename, "r")
        execution_time = -1.0
        process = -1
        for line in f:
            p = 0
            if "On process" in line:
                p = int(line.split(":")[1])
            elif "Execution time" in line:
                time = float(line.split(":")[1])
                if (time > execution_time):
                    process = p
                    execution_time = time
                    print "add" + str(execution_time)
                    if (len(time_list)-1 != i):
                        time_list.append(execution_time)
                    else:
                        time_list[i] = execution_time
                    if P == 1:
                        T_serial = execution_time
        i+=1
        print "---NUMBER OF PROCESSES "+str(P)+" ---"
        print "\tExecution time "+str(execution_time)
        print "\tReached for processors " + str(process)
        print "\tSpeed-up " + str(T_serial/execution_time)
        print "\tEfficiency " + str(T_serial/(execution_time*P))

    print time_list
    speed_up_list = [ time_list[0]/t for t in time_list]
    print speed_up_list
    plt.clf()
    plt.plot(p_list, speed_up_list)
    plt.savefig(os.path.join(dir, "speedup.png"))

if __name__ == "__main__":
    plot_speed_up(sys.argv[1])


