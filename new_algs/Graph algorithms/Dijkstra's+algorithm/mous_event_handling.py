import numpy as np
import cv2


def click_handler(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x) + ', ' + str(y);
        cv2.putText(img, strXY, (x, y), font, 1, (0, 0, 255), 1)
        cv2.imshow('image', img)
        print("({},{})".format(x,y))


img = cv2.imread('/Users/sheugumbie/Projects/OpenSource/opencv/opencv/samples/data/lena.jpg', -1)

cv2.imshow('image', img)

cv2.setMouseCallback('image', click_handler)
cv2.waitKey(0)
cv2.destroyAllWindows()
