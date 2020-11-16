import numpy as np
import matplotlib.pyplot as plt
from numpy import *
import matplotlib.animation as manimation
import time

start_time = time.time()

start_vertex, start_x, start_y, end_vertex, end_x, end_y, weight, c_x, c_y = np.genfromtxt(r'mst_data.txt', unpack=True)

plt.rcParams['animation.ffmpeg_path']='C:/Users/d-w-h/Downloads/ffmpeg-20200818-1c7e55d-win64-static/ffmpeg-20200818-1c7e55d-win64-static/bin/ffmpeg.exe'
writer=manimation.FFMpegWriter(bitrate=20000, fps=15)

fig = plt.figure(figsize=(8,8))
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
 
def animate(i):
    print(i)
    ax = plt.scatter(c_x, c_y, s=10, c='green')
    X = (start_x[i], end_x[i])
    Y = (start_y[i], end_y[i])
    cont = plt.plot(X, Y)

    return cont

size_t = size(start_vertex)
anim = manimation.FuncAnimation(fig, animate, frames=size_t, repeat=False)

print("Done Animation, start saving")

anim.save('test.mp4', writer=writer, dpi=200)
    
print("--- %s seconds ---" % (time.time() - start_time))
