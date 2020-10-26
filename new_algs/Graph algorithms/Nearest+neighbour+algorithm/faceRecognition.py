# Recognize Faces using some classification algorithm - like Logistic, KNN, SVM, etc

# 1. Load the training data (numpy arrays of all the persons)
        # x - values are stored in the numpy arrays
        # y - values we need to assign of face (int)
# 2. Read a video stream using OpenCV
# 3. Extract faces out of it
# 4. Use KNN to find the prediction of face (int)
# 5. Map the predicted id to name of the user
# 6. Display the predictions on the screen - bounding box and name

import cv2
import numpy as np
import os

# KNN Algorithm
def distance(v1, v2):
        # Euclidean
        return np.sqrt(((v1 - v2) ** 2).sum())

def KNN(train, test, K = 5):

        dist = []
        m = train.shape[0]

        for i in range(m):
                # Get the vector and label
                ix = train[i, :-1]
                iy = train[i, -1]

                #Compute the distance from test point
                d = distance(test, ix)
                dist.append([d, iy])

        # Sort based on distance and get top K
        dk = sorted(dist, key = lambda x : x[0])[: K]

        # Retrieve only the labels
        labels = np.array(dk)[:, -1]

        # Get frequencies of each label
        output = np.unique(labels, return_counts = True)

        # Find max frequency and corresponding label
        idx = np.argmax(output[1])
        
        return output[0][idx]

# Init Camera
cap = cv2.VideoCapture(0)

# Face Detection
faceCascade = cv2.CascadeClassifier('../files/haarcascade_frontalface_default.xml')

skip = 0
dataset_path = '../data/'
faceData = []
labels = []

classId = 0     # Label for the given file
names = {}      # Mapping between id - name

# Data Preparation
for fx in os.listdir(dataset_path):
        if fx.endswith('.npy'):

                # Create a mapping between class Id and names
                names[classId] = fx[:-4]

                data_item = np.load(dataset_path + fx)
                faceData.append(data_item)

                # Create Labels for the class
                target = classId * np.ones((data_item.shape[0], ))
                classId += 1
                labels.append(target)

faceDataset = np.concatenate(faceData, axis = 0)
faceLabels = np.concatenate(labels, axis = 0).reshape((-1, 1))

# print(faceDataset.shape)
# print(faceLabels.shape)

trainSet = np.concatenate((faceDataset, faceLabels), axis = 1)
# print(trainSet.shape)

# Testing

while True:
        ret, frame = cap.read()

        if ret == False:
                continue

        faces = faceCascade.detectMultiScale(frame, 1.3, 5)
        for (x, y, w, h) in faces:

                # Get the face region of interest
                offset = 10
                faceSection = frame[y - offset : y + h + offset, x - offset : x + w + offset]
                faceSection = cv2.resize(faceSection, (100, 100))

                out = KNN(trainSet, faceSection.flatten())

                # Display on the screen the name and rectangle around
                predName = names[int(out)]
                cv2.putText(frame, predName, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255))

        cv2.imshow("Faces", frame)

        key = cv2.waitKey(1) & 0xFF
        if(key == ord('q')):
                break

cap.release()
cv2.destroyAllWindows()

                 