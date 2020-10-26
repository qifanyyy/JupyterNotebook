import numpy as np
import subprocess
import random

N_CITIES = 500
MAX_CITIES = 1000000
X=(MAX_CITIES-N_CITIES*10)**(1/N_CITIES)
exp = [int(i*10+X**i) for i in range(1,N_CITIES+1)]

def run_command(bashCommand):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

for i, N in enumerate(exp):
    print("|",end='')
    rand = random.randint(1,10000) #Seed
    run_command("bash generator.sh "+str(N)+" "+str(rand)+" "+str(N))
