import cv2
import os
import numpy as np
import hungarian

alpha = 0.85
beta = 0.05

def remove_by_key(l,k):
    for i in range(len(l)):
        if l[i][1] == k:
            l.pop(i)
            return

def predict(first): # should take in position and velocity and output predicted position
    return [(i[0]+i[1]) for i in first]

def associate(first,next,method="greedy"): # take first and next position and return pair of index associated
    thresh = 50
    first = [(first[i],i) for i in range(len(first))]
    next = [(next[i],i) for i in range(len(next))]
    # print("first",first)
    # print("next",next)
    if method == "greedy":
        first = sorted(first, key=lambda x: np.sum(np.power(x[0][1],2)),reverse=True)
        pair = []
        for i in first:
            if len(next) != 0:
                distance = [np.sqrt(np.sum(np.power(n[0]-i[0],2))) for n in next]
                if np.min(distance) <= thresh:
                    pair.append([i[1],next[np.argmin(distance)][1]])
                    remove_by_key(next,next[np.argmin(distance)][1])
        return pair
    if method == "hungarian":
        k = max(len(first),len(next))
        dis_mat = np.zeros(shape=(k,k))
        for i in range(len(first)):
            for j in range(len(next)):
                dis_mat[i][j] = np.sqrt(np.sum(np.power(first[i][0] - next[j][0],2)))
        dis_mat[dis_mat>=thresh] = 10000
        solver = hungarian.Hungarian(dis_mat)
        solver.calculate()
        res = solver.get_results()
        ret = [i for i in res if dis_mat[i[0]][i[1]] < thresh]
        if len(first) > len(next):
            ret = [i for i in ret if i[1] < len(next)]
        if len(first) < len(next):
            ret = [i for i in ret if i[0] < len(first)]
        return ret


lpath = "Localization/"
l_files= os.listdir(lpath)
l_files.sort()
impath = "CS585-BatImages/FalseColor"
im_files= os.listdir(impath)
im_files.sort()

frame = []
for fname in l_files:
    subposition = []
    dir = "Localization/"+fname
    f = open(dir,"r")
    for i in f.readlines():
        res = i.split(",")
        if len(res) == 2:
            subposition.append([int(res[0]),int(res[1])])
    frame.append(subposition)

images = []
for iname in im_files:
    dir = "CS585-BatImages/FalseColor/"+iname
    im = cv2.imread(dir)
    images.append(im)
# initialize random color and zeros velocity

first = [(np.array(i), np.array([0, 0]), np.random.randint(256, size=(3))) for i in frame[0]]
canvas = np.zeros(shape=(1024, 1024, 3), dtype=np.uint8)
for frame_ind in range(len(frame)-1):
    predicted = predict(first)
    next = [np.array(j) for j in frame[frame_ind+1]]
    for n in next:
        cv2.circle(canvas,(n[0],n[1]),2,[0,0,255])
    pair = associate(predicted,next,method="hungarian")
    for p in pair:
        residual = next[p[1]] - first[p[0]][0]
        position = np.round(first[p[0]][0] + alpha * residual)
        position = position.astype(int)
        velocity = first[p[0]][1] + beta * residual
        next[p[1]] = (position,velocity,first[p[0]][2])
        cv2.line(canvas,tuple(first[p[0]][0].tolist()),tuple(next[p[1]][0].tolist()),tuple(first[p[0]][2].tolist()))
    for i in range(len(next)):
        if type(next[i]) != tuple:
            next[i] = (next[i], np.array([0,0]), np.random.randint(256,size=(3)))
    # print(first)
    # print(next)
    im = images[frame_ind+1]
    mask = cv2.bitwise_not(cv2.inRange(canvas,np.array([0,0,0],dtype=np.uint8),np.array([0,0,0],dtype=np.uint8)))
    im[mask] = 0
    im = im + canvas

    cv2.imwrite("output/f"+str(frame_ind)+".jpg",canvas)
    cv2.imwrite("output/g"+str(frame_ind)+".jpg",im)
    first = next

cv2.waitKey(0)