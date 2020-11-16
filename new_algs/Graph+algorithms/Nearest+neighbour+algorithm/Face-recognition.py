import cv2   #importing OpenCV
import numpy as np  #importing numpy as np
import os

#KNN Implementation

def distance(v1, v2):
	return np.sqrt(((v1-v2)**2).sum())

def knn(train, test, k=5):
	dist = []
	
	for i in range(train.shape[0]):
		ix = train[i, :-1]
		iy = train[i, -1]
		d = distance(test, ix)
		dist.append([d, iy])

    #Sort on the basis of distance    
	dk = sorted(dist, key=lambda x: x[0])[:k]
	labels = np.array(dk)[:, -1]

    #Frequency of each label
	output = np.unique(labels, return_counts=True)
    #Maximum frequency and its label
	index = np.argmax(output[1])
	return output[0][index]

#Capturing Video from webcam
# 0 represent the default camera of system
cap = cv2.VideoCapture(0) 
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

skip = 0
dataset_path = './data/'
face_data = []
labels=[]
class_id=0
names={}

#Data Preparation

for fx in os.listdir(dataset_path):
    if fx.endswith('.npy'):
        names[class_id]= fx[:-4]
        print("Loaded"+fx)
        data_item=np.load(dataset_path+fx)
        face_data.append(data_item)

        target=class_id*np.ones((data_item.shape[0],))
        class_id+=1
        labels.append(target)

face_dataset=np.concatenate(face_data,axis=0)
face_labels=np.concatenate(labels,axis=0).reshape((-1,1))

print(face_dataset.shape)
print(face_labels.shape)

trainset=np.concatenate((face_dataset,face_labels),axis=1)
print(trainset.shape)

#Testing part

while True :
    ret,frame = cap.read() #string the caputring video frame

    if ret == False : #if no frame captured then loop is continued
        continue

    faces = face_cascade.detectMultiScale(frame,1.3,5)
    
    for face in faces :
        x,y,w,h = face
       
        
       #Extraction of required face area
        offset = 10
        face_section = frame[y-offset:y+offset+h , x-offset:x+offset+w]
        face_section = cv2.resize(face_section,(100,100))
        
        out=knn(trainset,face_section.flatten())

        pred_name=names[int(out)]

        cv2.putText(frame,pred_name,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)

    cv2.imshow("Faces",frame)

    key_pressed = cv2.waitKey(1) & 0xFF 
    if key_pressed == ord('q') : #terminate the program when q is pressed
        break 
cap.release()         
cv2.destroyAllWindows()






