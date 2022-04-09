import numpy as np
import cv2
from hsv_256 import hsv_256
# detects coke can
# please don't be annoying
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red1 = np.array(hsv_256([0, 40, 50]))
    upper_red1 = np.array(hsv_256([30, 100, 100]))
    lower_red2 = np.array(hsv_256([330, 40, 50]))
    upper_red2 = np.array(hsv_256([360, 100, 100]))

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2= cv2.inRange(hsv, lower_red2, upper_red2)

    mask = cv2.bitwise_or(mask1, mask2)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('sodas', result)

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()