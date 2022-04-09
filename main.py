from cv2 import COLOR_BGR2GRAY
import numpy as np
import cv2
from hsv_256 import hsv_256
import time
# detects coke can
# it works woo
cap = cv2.VideoCapture(0)

width = int(cap.get(3))
height = int(cap.get(4))
contrast = np.zeros((height, width, 3), np.uint8)
contrast[:] = (0, 0, 0)


while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red1 = np.array(hsv_256([0, 40, 50]))
    upper_red1 = np.array(hsv_256([30, 100, 100]))
    lower_red2 = np.array(hsv_256([330, 40, 50]))
    upper_red2 = np.array(hsv_256([360, 100, 100]))

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2= cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    royalmask = cv2.bitwise_and(frame, frame, mask=mask)

    blackroyal = cv2.cvtColor(royalmask, COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(blackroyal, 20, 0.01, 20)
    if (corners is not None):
        corners = np.int0(corners)
    else:
        corners = np.array([])

    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(royalmask, (x,y), 5, (255,255,255), -1)

    cv2.imshow('sodas', royalmask)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()