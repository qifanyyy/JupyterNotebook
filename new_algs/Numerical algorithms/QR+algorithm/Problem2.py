#!/usr/bin/env python
# coding: utf-8

# In[45]:


import matplotlib.pyplot as plt
import numpy as np
from scipy import signal 

def notch_filter(data):
    fs = 256.0  # sample frequency (Hz)
    f0 = 50.0  # frequency to be removed from signal (Hz)
    Q = 30.0  # quality factor
    w0 = f0/(fs/2)  # normalized frequency
    i, u = signal.iirnotch(w0,Q)
    y = signal.lfilter(i, u, data)
    return y

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

def differenciate(ecg_signal):
    output = np.zeros(len(ecg_signal))
    t=1/256
    for i in range(0,len(ecg_signal)):
        if(i>1 and i<(len(ecg_signal)-2)):
            output[i] = (0.125*t)*((-1*ecg_signal[i-2])+(-2*ecg_signal[i-1])+(2*ecg_signal[i+1])+(ecg_signal[i+2]))
        elif(i<(len(ecg_signal)-2)): #first or second sample
            if(i==0): #sample @ index 0
                output[i] = (0.125*t)*((2*ecg_signal[i+1])+(ecg_signal[i+2]))
            else: #sample @ index 1
                output[i] = (0.125*t)*((-2*ecg_signal[i-1])+(2*ecg_signal[i+1])+(ecg_signal[i+2]))
        elif(i>1): #last or before last sample
            if(i==(len(ecg_signal)-1)): #last sample 
                output[i] = (0.125*t)*((-1*ecg_signal[i-2])+(-2*ecg_signal[i-1]))
            else: #before last sample
                output[i] = (0.125*t)*((-1*ecg_signal[i-2])+(-2*ecg_signal[i-1])+(2*ecg_signal[i+1]))
    return output

def square(ecg_signal):
    output = np.zeros(len(ecg_signal))
    for i in range(0,len(ecg_signal)):
        output[i] = pow(ecg_signal[i],2)         
    return output  

def smooth(ecg_signal,n):
    result = np.zeros(len(ecg_signal))
    for i in range(0,len(ecg_signal)):
        sum=0
        for j in range(0,n):
            if(i+j<len(ecg_signal)):
                sum += ecg_signal[i+j]  
        result[i] = sum*(1/n)
        i+=n
    return result

def thresholding(ecg_signal):
    result = np.zeros(len(ecg_signal))
    min=np.amin(ecg_signal)
    max=np.amax(ecg_signal)
    threshold=(max-min)*0.7
    return threshold    
        
def ecg_plot(y):
    x = np.zeros(len(y))
    for i in range(0,len(y)):
        if(i>0):
            x[i] = x[i-1] + 0.003906 
    a = x[0:2000]
    b = y[0:2000]
#     plt.plot(a,b)
#     plt.xlabel("Time/sec")
#     plt.ylabel("Signal value/Volts")
#     plt.savefig ('Name.jpg')

def final_plot(y,threshold):
    x = np.zeros(len(y))
    for i in range(0,len(y)):
        if(i>0):
            x[i] = x[i-1] + 0.003906 
    a = x
    b = y
    
    threshold_passing_indices = np.where(b>threshold)
    threshold_passing_indices_array = threshold_passing_indices[0]
    sum1 = 0
    num_of_elements = 0
    avg = 0
    r_indices = np.array([])
    r_indices = r_indices.astype(int)
    for i in range(0,len(threshold_passing_indices_array)):
        if(i==(len(threshold_passing_indices_array)-1)): #last element
            sum1 += threshold_passing_indices_array[i]
            num_of_elements += 1
            avg = sum1//num_of_elements
            r_indices = np.append(r_indices,avg)
        elif(threshold_passing_indices_array[i+1]-threshold_passing_indices_array[i]==1):
            sum1 += threshold_passing_indices_array[i]
            num_of_elements += 1
        else:
            sum1 += threshold_passing_indices_array[i]
            num_of_elements += 1
            avg = sum1//num_of_elements
            r_indices = np.append(r_indices,avg)
            num_of_elements = 0
            sum1 = 0
            avg = 0
    #Creating a boolean array equal to the size of the samples, with True at the R-wave positions only
    r_boolean_markers = np.zeros(len(a), dtype=bool)
    for i in range(0,len(r_indices)):
        r_wave_index = r_indices[i]
        r_boolean_markers[r_wave_index] = True  
#     plt.plot(a, b, '-gD', markevery = r_boolean_markers.tolist(), marker='*')
#     plt.xlabel("Time/sec")
#     plt.ylabel("Signal value/Volts")
#     plt.savefig ('25_prob2.jpg')
    
    #rr plot
    timestamps = np.array([])
    timestamps = timestamps.astype(int)
    for i in range(0,len(r_indices)):
        timestamps = np.append(timestamps,x[r_indices[i]])
    rr_intervals = np.array([])
    for i in range(0,(len(timestamps)-1)):
        diff = timestamps[i+1]-timestamps[i]
        rr_intervals = np.append(rr_intervals,diff)
    rr_x = np.array([])
    for i in range(0,len(rr_intervals)):
        rr_x = np.append(rr_x,i)   
    msec_interval = 1000*(rr_intervals)
#     plt.plot(rr_x, msec_interval)
#     plt.savefig ('RR.jpg')
    return (msec_interval,timestamps)        
    
def qrs_detect(ecg_signal, n):
#     ecg_plot(ecg_signal)
    notch_filtered = notch_filter(ecg_signal)
#     ecg_plot(notch_filtered)
    bandpass_filtered = butter_bandpass_filter(notch_filtered, 0.1, 45, 256, order=5)
#     ecg_plot(bandpass_filtered)
    differenciated = differenciate(bandpass_filtered)
#     ecg_plot(differenciated)
    squared = square(differenciated)
#     ecg_plot(squared)
    smoothed= smooth(squared,n)
#     ecg_plot(smoothed)
    threshold = thresholding(smoothed)
    msec_interval,timestamps = final_plot(smoothed,threshold)
    return (msec_interval,timestamps)

def missing_beat_detection(ecg_signal,n):
    msec_interval,timestamps = qrs_detect(ecg_signal,n)
    avg_interval = np.mean(msec_interval)
    missing_beats = np.array([])
    for i in range(0,len(msec_interval)):
        if(msec_interval[i]>(1.5*avg_interval)): #a missing beat
            timestamp = (timestamps[i+1] + timestamps[i])/2
            missing_beats = np.append(missing_beats,timestamp)
    return missing_beats
    
if __name__ == "__main__":
    #read the ECG signal values into a np array
    ecg_signal = np.loadtxt(fname = "Data2.txt")
    missing_beats = missing_beat_detection(ecg_signal,25)
    file = open("MissingBeats.txt","w")
    output = np.array2string(missing_beats)
    file.write(output)
    file.close()


# In[ ]:




