import os
import multiprocessing as mp
import pdb
from time import *
import threading
import subprocess as sp


def run_auto(f):
    try:
        cmd = 'python shortest_path.py -f ' +  directory + '/' + f + ' -i 1000'
        #os.system('python shortest_path.py -f ' +  directory + '/' + f + ' -i 1000 > data/' + alg[1] + '/' + alg[-1] + '/rawdata_0/' + f)
        #cmd = 'python shortest_path.py'
        #arg1 = '-f'
        #arg2 = directory + '/' + f 
        #arg3 = '-i'
        #arg4 = '1000'

        out = sp.check_output(cmd, shell=True)
        s = []
        s.append(f)
        s.append(out)
        return s
        
    except sp.CalledProcessError:
        print '-----CalledProcessError-----'

    except:
        print "-----Error-----"
        print directory + '/' + f

  

    return directory + '/' + f + '   -----Done-----'



while True:
    try:
        directory = raw_input('Enter the input directory: ')
        if directory[:5] == 'input':
            break
        else:
            print 'Try Again...'
    except:
        print 'Try Again...'
    
start = time()

if directory[-1:] == '/':
    directory = directory[:-1]
        

alg = directory.split('/')

dirs = os.listdir(directory)

#q = mp.Queue()
results = []

pool = mp.Pool(processes = 4)
#output = [pool.map(run_auto, f) for f in dirs]
#results = [pool.apply_async(run_auto, args=(f)) for f in dirs]

for f in dirs:
    #pdb.set_trace()
    results.append(pool.apply_async(run_auto, args=(f,)))



for i in results:
    item = i.get()
    outfile = open('data/' + alg[1] + '/' + alg[-1] + '/rawdata_0/' + item[0], 'wb')

    outfile.write(item[1])
    outfile.close()



#for f in dirs:
    #run_auto(f)

end = time()

#print 'Length of queue: ' + q.qsize()

print 'Time: ' + str(end - start)
