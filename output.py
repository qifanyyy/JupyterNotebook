import os
dir_name = "/data/stairs/JupyterNB/algorithms2/"
with open("/data/stairs/JupyterNB/result_part2.txt", "w") as output:
        for folder in os.listdir(dir_name):
            if os.path.isdir(dir_name + folder + '/'):
                length = len(os.listdir(dir_name + folder + '/'))
                print("alg = ", folder, " its length = ", length)
                output.write(folder + '-------->' + " " + str(length) + "\n")