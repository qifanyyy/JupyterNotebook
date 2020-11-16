import cv2;
import numpy as np;

#https://docs.opencv.org/3.1.0/dc/d2e/tutorial_py_image_display.html
#
input = cv2.imread('templates/test.jpg', cv2.IMREAD_COLOR);

version = "Laplace";

if version == "Laplace":
    mode = cv2.IMREAD_GRAYSCALE;
else:
    mode = cv2.IMREAD_COLOR;

#Templates to match against
#In normal mode it will use the colored images
#In Laplace mode it will use the grayscale images that highlight the edges
if mode == cv2.IMREAD_COLOR:
    template_5 = cv2.imread('templates/5_szamc.png', mode);
    template_10 = cv2.imread('templates/10_szamc.png', mode);
    template_20 = cv2.imread('templates/20_szamc.png', mode);
    template_50 = cv2.imread('templates/50_szamc.png', mode);
    template_100 = cv2.imread('templates/100_szamc.png', mode);
    template_200 = cv2.imread('templates/200_szamc.png', mode);
if mode == cv2.IMREAD_GRAYSCALE:
    template_5 = cv2.imread('templates/5_szam.png', mode);
    template_10 = cv2.imread('templates/10_szam.png', mode);
    template_20 = cv2.imread('templates/20_szam.png', mode);
    template_50 = cv2.imread('templates/50_szam.png', mode);
    template_100 = cv2.imread('templates/100_szam.png', mode);
    template_200 = cv2.imread('templates/200_szam.png', mode);
#Coins in order of size
templates = [template_5, template_100, template_10, template_20, template_50, template_200];
#Coin values
template_values = [5, 100, 10, 20, 50, 200, 0];
#Coin radius multipliers
template_scaling = [1.13513, 1.03, 1.09524, 1.04348, 1.0496, 1.0981];

#Inverting and smoothing template images
if mode == cv2.IMREAD_GRAYSCALE:
    for template in templates:
        template = cv2.GaussianBlur(template, (3, 3), 0);
        template = cv2.bitwise_not(template);

kernel = np.ones((5,5), np.uint8);
width = input.shape[1];
height = input.shape[0];

blur = cv2.GaussianBlur(input, (3,3), 0);
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY);
_, filtered = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU);
filtered = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, kernel);
filterEdges = cv2.Canny(filtered, 10, 100);
#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);

edges = cv2.Laplacian(gray, cv2.CV_64F);
edges = cv2.convertScaleAbs(edges);
mask = np.zeros((gray.shape[0], gray.shape[1]), np.uint8);

#https://docs.opencv.org/3.1.0/da/d53/tutorial_py_houghcircles.html
circles = cv2.HoughCircles(filterEdges, cv2.HOUGH_GRADIENT, 1, 70, param1=60, param2=30, minRadius=20, maxRadius=160);

original = np.copy(input);

matches = [];
bestIndices = [];
#NORMAL TEMPLATE MATCHING
for index, i in enumerate(circles[0,:]):
    cv2.circle(input,(i[0],i[1]),i[2],(0,128,255),2)
    bestMatchIndex = -1;
    bestMatch = 0.0;
    matches.append([]);
    for k, template in enumerate(templates):
        resized = cv2.resize(template, None, fx=i[2]*2/template.shape[0], fy=i[2]*2/template.shape[0], interpolation = cv2.INTER_CUBIC);
        if version == "Laplace":
            resized = cv2.Laplacian(resized, cv2.CV_64F);
            resized = cv2.convertScaleAbs(resized);
            res = cv2.matchTemplate(edges,resized,cv2.TM_CCOEFF_NORMED);
        else:
            res = cv2.matchTemplate(original,resized,cv2.TM_CCOEFF_NORMED);
        prob = res[int(i[1]-i[2])][int(i[0]-i[2])];
        matches[index].append(prob);
        cv2.putText(input, "{:.3f}".format(prob), (int(i[0]-0.7*i[2]), int(i[1]-i[2]*0.4+k*14)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1, cv2.LINE_AA);
        if prob > bestMatch:
            bestMatch = prob;
            bestMatchIndex = k;
    bestIndices.append(bestMatchIndex);
    cv2.putText(input, "{:d}".format(template_values[bestMatchIndex]), (int(i[0]+i[2]*0.6), int(i[1]-i[2] * 0.5)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 1, cv2.LINE_AA);
    cv2.putText(input, "{:.1f}".format(i[2]), (int(i[0]+i[2]*0.9), int(i[1]-i[2] * 0.2)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1, cv2.LINE_AA);
#Confidence for each coin on the picture
confidence = [];
highestConfidenceIndex = 0;
for r in range(0, len(bestIndices)):
    sqrdiff = 0.0;
    for i, match in enumerate(matches[r]):
        if r != i:
            #The confidence level is based on the difference from the highest probability coin
            diff = abs(matches[r][bestIndices[r]] - matches[r][i]);
            sqrdiff += diff;
    confidence.append(sqrdiff);
    if sqrdiff > confidence[highestConfidenceIndex]:
        highestConfidenceIndex = r;
#print the confidence on each coin
for k, c in enumerate(confidence):
    circle = circles[0][k];
    cv2.putText(input, "{:.2f}".format(c), (int(circle[0]), int(circle[1]-circle[2])), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1, cv2.LINE_AA);

#Calculate the radius of each coin type based on the radius of the known coin.
meanRadius = [None] * len(templates);
#The known radius
meanRadius[bestIndices[highestConfidenceIndex]] = circles[0][highestConfidenceIndex][2];
if bestIndices[highestConfidenceIndex] > 0:
    for k in range(bestIndices[highestConfidenceIndex]-1, -1, -1):
        meanRadius[k] = meanRadius[k+1] / template_scaling[k];
if bestIndices[highestConfidenceIndex] < len(templates):
    for k in range(bestIndices[highestConfidenceIndex]+1, len(templates)):
        meanRadius[k] = meanRadius[k-1] * template_scaling[k];

#Print the coin type on each coin, based on the minimal difference in radius to each predicted coin radius
for k, circle in enumerate(circles[0,:]):
    bestIndex = 0;
    for i, mean in enumerate(meanRadius):
        diff = abs(circle[2] - mean);
        if diff < circle[2] - meanRadius[bestIndex]:
            bestIndex = i;
    cv2.putText(input, "{:d}".format(template_values[bestIndex]), (int(circle[0]+circle[2]), int(circle[1]-circle[2])), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1, cv2.LINE_AA);


#display the resulting frame
cv2.imshow('gray', gray);
cv2.imshow('laplacian', edges);
cv2.imshow('coins', filterEdges);
cv2.imshow('detect', input);
cv2.waitKey(0);
cv2.destroyAllWindows()
