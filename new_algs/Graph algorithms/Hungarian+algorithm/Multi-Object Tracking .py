#!/usr/bin/env python
# coding: utf-8

# In[4]:


from numpy import *
from numpy import round
import numpy as np
import cv2
import copy
import numpy as np
from scipy.optimize import linear_sum_assignment
from munkres import Munkres
from math import floor

kernel = np.array([[1,1,0,0],[0,1,1,0],[0,1,1,1],[0,0,1,1]],np.uint8)
kernel = kernel + np.flip(kernel,0)
kernel_e = np.array([[0,0,0,0,0,0,0],[0,0,0,1,1,0,0],[1,1,1,1,1,1,0],[0,0,1,1,0,0,0],[0,0,0,0,0,0,0]],np.uint8)
kernel_e = kernel_e + np.flip(kernel_e,0)
kernel_d1 = np.array([[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0]],np.uint8)
kernel_d2 = np.array([[0,0,0,0,0],[0,0,1,0,0],[0,1,1,1,0],[0,0,1,0,0],[0,0,0,0,0]],np.uint8)


# In[5]:


class KalmanFilter(object):
    def __init__(self):
        self.dt = 0.005
        self.A = array([[1, 0], [0, 1]])  
        self.u = zeros((2, 1))  
        self.b = array([[0], [255]])  
        self.P = diag((3.0, 3.0))  
        self.F = array([[1.0, self.dt], [0.0, 1.0]])  
        self.Q = eye(self.u.shape[0])  
        self.R = eye(self.b.shape[0])  
        self.lastResult = array([[0], [255]])

    def predict(self):
        self.u = np.round(dot(self.F, self.u))
        self.P = dot(self.F, dot(self.P, self.F.T)) + self.Q
        self.lastResult = self.u  
        return self.u

    def correct(self, b, flag):
        if not flag:  
            self.b = self.lastResult
        else:  
            self.b = b
        C = dot(self.A, dot(self.P, self.A.T)) + self.R
        K = dot(self.P, dot(self.A.T, linalg.inv(C)))

        self.u = round(self.u + dot(K, (self.b - dot(self.A,self.u))))
        self.P = self.P - dot(K, dot(C, K.T))
        self.lastResult = self.u
        return self.u


# In[6]:


class Detectors(object):
    def __init__(self):
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=250, varThreshold=60,detectShadows=False)

    def Detect(self, frame):
        
        ## Back ground subtraction
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = self.fgbg.apply(gray)
        H,W,_ = frame.shape
        demag = 30
        Win_H = floor(H*demag/100)
        Win_W = floor(W*demag/100)
        cv2.imshow('Bg Subtraction', mask)
        
        
        ## Morphological Operaations 
        erosion = cv2.erode(mask,kernel_e,iterations = 1)
        dilation = cv2.dilate(erosion,kernel_d1,iterations = 6)
        #dilation = cv2.dilate(erosion,kernel_d1,iterations = 6)
        
        ret, thresh = cv2.threshold(dilation, 250, 255, 0)

        _, contours, hierarchy = cv2.findContours(thresh,
                                                  cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.imshow('Morphological Operation', thresh)
        centers = [] 
        #r_thresh = 60 #for ball
        r_thresh = 14 #fro random walk
        #r_thresh = 30 #for town centre
        
        for cnt in contours:
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                centeroid = (int(x), int(y))
                radius = int(radius)
                if (radius > r_thresh):
                    cv2.circle(frame, centeroid, radius, (0, 255, 0), 2)
                    b = np.array([[x], [y]])
                    centers.append(np.round(b))
        return centers


# In[7]:


class Track(object):

    def __init__(self, prediction, trackIdCount):
        self.track_id = trackIdCount  
        self.KF = KalmanFilter()  
        self.prediction = np.asarray(prediction) 
        self.skipped_frames = 0 
        self.trace = [] 

class Tracker(object):
    def __init__(self, dist_thresh, max_frames_to_skip, max_trace_length,
                 trackIdCount):
        self.dist_thresh = dist_thresh
        self.max_frames_to_skip = max_frames_to_skip
        self.max_trace_length = max_trace_length
        self.tracks = []
        self.trackIdCount = trackIdCount

    def Update(self, detections):
        
        if (len(self.tracks) == 0):
            for i in range(len(detections)):
                track = Track(detections[i], self.trackIdCount)
                self.trackIdCount += 1
                self.tracks.append(track)

       
        N = len(self.tracks)
        M = len(detections)
        # Finding Cost then applying Hungarian Algorithm
        cost = np.zeros(shape=(N, M)) 
        for i in range(len(self.tracks)):
            for j in range(len(detections)):
                try:
                    diff = self.tracks[i].prediction - detections[j]
                    distance = np.sqrt(diff[0][0]*diff[0][0] +
                                       diff[1][0]*diff[1][0])
                    cost[i][j] = distance
                except:
                    pass

        cost = (0.5)*cost
       
        assignment = []
        for _ in range(N):
            assignment.append(-1)
        hungarian = Munkres()

        #index = hungarian.compute(cost)
        row_ind, col_ind = linear_sum_assignment(cost)
        
        for i in range(len(row_ind)):
            assignment[row_ind[i]] = col_ind[i]

        
        un_assigned_tracks = []
        for i in range(len(assignment)):
            if (assignment[i] != -1):
               
                if (cost[i][assignment[i]] > self.dist_thresh):
                    assignment[i] = -1
                    un_assigned_tracks.append(i)
                pass
            else:
                self.tracks[i].skipped_frames += 1

       
        del_tracks = []
        for i in range(len(self.tracks)):
            if (self.tracks[i].skipped_frames > self.max_frames_to_skip):
                del_tracks.append(i)
        if len(del_tracks) > 0:  
            for id in del_tracks:
                if id < len(self.tracks):
                    del self.tracks[id]
                    del assignment[id]
                else:
                    print("Error in deleting tracks")

       
        un_assigned_detects = []
        for i in range(len(detections)):
                if i not in assignment:
                    un_assigned_detects.append(i)

        
        if(len(un_assigned_detects) != 0):
            for i in range(len(un_assigned_detects)):
                track = Track(detections[un_assigned_detects[i]],
                              self.trackIdCount)
                self.trackIdCount += 1
                self.tracks.append(track)

        for i in range(len(assignment)):
            self.tracks[i].KF.predict()

            if(assignment[i] != -1):
                self.tracks[i].skipped_frames = 0
                self.tracks[i].prediction = self.tracks[i].KF.correct(
                                            detections[assignment[i]], 1)
            else:
                self.tracks[i].prediction = self.tracks[i].KF.correct(
                                            np.array([[0], [0]]), 0)

            if(len(self.tracks[i].trace) > self.max_trace_length):
                for j in range(len(self.tracks[i].trace) -
                               self.max_trace_length):
                    del self.tracks[i].trace[j]

            self.tracks[i].trace.append(self.tracks[i].prediction)
            self.tracks[i].KF.lastResult = self.tracks[i].prediction


# In[16]:


def start_tracking():

    detector = Detectors()
    tracker = Tracker(60, 20, 50, 1)
    track_colors = [(128,0,0), (140, 255, 0), (0, 40, 255), (50, 255, 50),
                    (0, 255, 255), (255, 0, 255), (255, 127, 255),
                    (127, 0, 255), (127, 0, 127),(0,0,139),(255,20,147),(210,105,30),(112,128,144)]
    
    
    
    success, frame = vidcap.read()
    H,W,_ = frame.shape
    demag = 100

    Win_H = floor(H*demag/100)
    Win_W = floor(W*demag/100)

    cv2.namedWindow('BgSubtraction',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('BgSubtraction',Win_W,Win_H)
    cv2.namedWindow('Morphological Operation',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Morphological Operation', Win_W,Win_H)
    
    out = cv2.VideoWriter('C:/Users/dell pc/Desktop/outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (Win_W,Win_H))

    
    while(success):
        success, frame = vidcap.read()
        orig_frame = copy.copy(frame)
        centers = detector.Detect(frame)
        if (len(centers) > 0):
            tracker.Update(centers)
            for i in range(len(tracker.tracks)):
                if (len(tracker.tracks[i].trace) > 1):
                    for j in range(len(tracker.tracks[i].trace)-1):
                        # Draw trace line
                        x1 = tracker.tracks[i].trace[j][0][0]
                        y1 = tracker.tracks[i].trace[j][1][0]
                        x2 = tracker.tracks[i].trace[j+1][0][0]
                        y2 = tracker.tracks[i].trace[j+1][1][0]
                        clr = tracker.tracks[i].track_id % 13
                        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                 track_colors[clr], 2)
            
            cv2.namedWindow('Tracking',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Tracking', Win_W,Win_H)
            cv2.imshow('Tracking', frame)
            out.write(frame)
            
        cv2.namedWindow('Original',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Original', Win_W,Win_H)
        cv2.imshow('Original', orig_frame)
        cv2.waitKey(1)

    vidcap.release()
    cv2.destroyAllWindows()


# In[17]:


if __name__=="__main__":
    import sys
    args = sys.argv[1]
    vidcap = cv2.VideoCapture(args)
    start_tracking()
    



