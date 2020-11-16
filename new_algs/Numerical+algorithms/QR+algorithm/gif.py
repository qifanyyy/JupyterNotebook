from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy import interpolate

import seaborn as sns

# initializing a figure in  
# which the graph will be plotted 
fig = plt.figure()
fig.set_size_inches(11, 7)
# marking the x-axis and y-axis

axis = plt.axes(xlim=(2, 51), ylim=(20, 130))
axis.spines["top"].set_visible(False)
axis.spines["bottom"].set_visible(False)
axis.spines["right"].set_visible(False)
axis.spines["left"].set_visible(False)

axis.get_xaxis().tick_bottom()
axis.get_yaxis().tick_left()

axis.xaxis.set_tick_params(length=0)
axis.yaxis.set_tick_params(length=0)
sns.despine(left=True, bottom=True)
# initializing a line variable
colors = [(31/255., 119/255., 180/255.), (174/255., 199/255., 232/255.), (255/255., 127/255., 14/255.)]
colors = [(214/255., 39/255., 40/255.), (255/255., 152/255., 150/255.)]

line1, = axis.plot([], [], lw=2, label='QR_unshifted', color=colors[0])
line2, = axis.plot([], [], lw=2, label='QR_shifted',color=colors[1])
#line3, = axis.plot([], [], lw=2, label='QR_wilkinson_shifted',color=colors[2])
lines = [line1, line2]
top_dim = 50
step = 1
dim_list = [2 + step * i for i in range(top_dim)]
QR_unshifted= [12.93,25.48,26.44,32.23,43.48,39.73,48.46,60.13,53.43,55.41,63.06,74.95,72.89,75.53,66.93,76.95,76.87,65.29,83.01,79.34,85.97,87.45,94.26,99.73,105.33,97.89,89.78,81.3,90.39,97.71,100.99,101.16,103.94,106.81,109.09,104.86,111.84,106.26,101.91,119.59,110.25,113.29,126.59,115.9,135.29,125.56,113.53,121.24,135.29,124.02]
QR_shifted=[3.3,15.26,15.08,26.39,30.45,31.45,37.61,38.9,53.22,68.04,47.35,45.54,61.56,57.38,86.54,68.68,57.01,51.87,77.28,78.35,63.45,84.23,63.29,76.35,68.25,73.48,63.93,86.67,125.34,114.27,75.04,92.86,77.34,86.8,87.48,111.44,91.08,86.53,75.42,85.98,142.92,81.23,102.66,129.58,97.07,97.23,85.7,94.55,112.6,95.48]
QR_wilkinson_shift=[1.96,14.95,15.5,22.83,31.05,29.11,35.92,37.51,59.12,60.32,43.04,53.86,55.58,61.19,79.21,69.26,59.92,53.12,82.69,61.89,63.47,84.22,66.89,80.83,66.9,65.52,69.36,79.23,79.94,84.79,70.35,75.68,68.88,74.96,83.97,79.65,86.8,94.1,74.14,101.38,134.45,87.55,84.94,89.88,92.88,98.61,91.55,94.35,122.14,115.25]
H_QR_unshifted=[12.93,25.48,26.44,32.23,43.48,39.73,48.46,60.13,53.43,55.41,63.06,74.95,72.89,75.53,66.93,76.95,76.87,65.29,83.01,79.34,85.97,87.45,94.26,99.73,105.33,97.89,89.78,81.3,90.39,97.71,100.99,101.16,103.94,106.81,109.09,104.86,111.84,106.26,101.91,119.59,110.25,113.29,126.59,115.9,135.29,125.56,113.53,121.24,135.29,124.02]
H_QR_shifted=[3.3,9.72,13.85,26.72,25.82,27.89,33.13,48.49,38.99,49.3,48.18,51.88,55.64,59.41,49.53,67.07,58.87,58.31,71.6,88.9,80.35,66.27,78.08,64.3,82.94,80.4,68.3,77.02,88.49,115.74,67.04,84.18,92.47,81.94,86.28,91.56,83.72,88.25,75.63,79.9,89.31,98.78,78.58,99.73,104.12,96.49,91.5,96.07,98.89,89.93]
H_QR_wilkinson_shift=[1.96,9.05,14.52,23.13,30.39,29.17,32.76,46.7,38.7,44.53,46.44,52.27,49.09,59.14,49.6,65.49,61.11,57.72,72.48,89.58,80.29,66.08,73.13,65.6,82.13,81.09,68.06,75.21,77.68,83.16,65.62,84.64,90.52,84.49,87.38,93.85,88.13,116.95,77.52,80.2,89.05,98.2,82.15,99.68,101.08,95.12,92.07,100.4,99.56,90.6]


x_base = np.linspace(2, 51, 400)
a_BSpline_QR_unshifted = interpolate.make_interp_spline(dim_list, QR_unshifted)
a_BSpline_QR_shifted = interpolate.make_interp_spline(dim_list, QR_shifted)
a_BSpline_QR_wilkinson_shift = interpolate.make_interp_spline(dim_list, QR_wilkinson_shift)
y_base_QR_unshifted = a_BSpline_QR_unshifted(x_base)
y_base_QR_shifted = a_BSpline_QR_shifted(x_base)
y_base_QR_wilkinson_shift = a_BSpline_QR_wilkinson_shift(x_base)
xdata = []
ydata1 = []
ydata2 = []
ydata3 = []
# data which the line will
# contain (x, y) 
def init():
    for line in lines:
        line.set_data([], [])
    return lines

def animate(i):
    xdata.append(x_base[i])
    # plots a sine graph 
    ydata1.append(y_base_QR_unshifted[i])
    ydata2.append(y_base_QR_shifted[i])
    #ydata3.append(y_base_QR_wilkinson_shift[i])
    line1.set_data(xdata, ydata1)
    line2.set_data(xdata, ydata2)
    #line3.set_data(xdata, ydata3)
    return lines


anim = FuncAnimation(fig, animate, init_func=init, frames=399, interval=20, blit=True)
axis.legend(frameon=False)
plt.title("QR with/without Shift")
anim.save('gif_shift_final_data.mp4', writer='ffmpeg', fps=30)