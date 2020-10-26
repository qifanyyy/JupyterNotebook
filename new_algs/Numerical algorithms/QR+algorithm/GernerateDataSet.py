import random
from string import ascii_lowercase
import os.path

def generate(lines, columns):

    random.seed()

    #save_path = 'P:/licenta/QR_SearchingAlgorithm'

    #completeName = os.path.join(save_path, name_of_file + ".txt")

    file = open("P:\licenta\QR_SearchingAlgorithm\DataSetG.txt", "w+")
    file2 = open("P:\licenta\QR_SearchingAlgorithm\Debug\DataSetG.txt", "w+")
    n = 3
    for j in range (columns):
        string_val = "".join(random.choice(ascii_lowercase) for i in range(n))
        file.write('%6s  ' % (string_val, ))
        file2.write('%6s  ' % (string_val,))

    for i in range (1, lines):
        file.write("\n")
        file2.write("\n")
        for j in range (columns):
            r = round(random.uniform(0, 900), 2)
            file.write('%06.2f  ' %(r))
            file2.write('%06.2f  ' % (r))


    file.close()
    file2.close()


generate(30, 20)


