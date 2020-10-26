# libraries
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# pop_pakistan = [44.91, 58.09, 78.07, 107.7, 138.5, 170.6]
# plt.plot(pop_pakistan, color='g')
# plt.xlabel('Countries')
# plt.ylabel('Population in million')
# plt.title('Pakistan India Population till 2010')
# #plt.show()
#
# plt.savefig('foo.png', bbox_inches='tight')

import os, sys, getopt
import matplotlib.pyplot as plt
import seaborn as sns

def handleArgs(argv):
    if(len(argv) < 2):
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, "i:c:")
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i"):
            input = arg;
        elif opt in ("-c"):
            column = int(arg);
        else:
            sys.exit()

    return input, column

# -i "outputs/simple/simple_g1000_p50_m0.8_c0.8_e0.2.csv" -o "outputs/simple/"

def main(argv):
    input, column = handleArgs(argv)

    output = input.replace(".csv", ".png")

    f = open(input, "r")
    data = []

    type = 0

    for line in f:
        if line[0] == 'h':
            # header
            type = (line.split(",")[column]).replace(" ", "")
        elif line[0] != 'i':
            lineSplit = line.split()
            data.append(lineSplit[column])

    inputSplit = input.split("/")
    name = inputSplit[len(inputSplit)-1]
    name = name.replace(".csv", "")

    plt.plot(data, color='g')
    plt.xlabel('Generations')
    plt.ylabel(type)
    plt.title(name)

    output = input.replace(".csv", "_" + str(type) + ".png")
    print("Generating plot for {0}, type {1}".format(name, type))
    savePath = output;
    plt.savefig(savePath, bbox_inches='tight')

if __name__ == "__main__":
   main(sys.argv[1:])
