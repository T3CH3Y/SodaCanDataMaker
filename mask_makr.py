import numpy as np
from hsv_256 import hsv_256
import cv2

def mask_makr(frame, colorVal1, colorVal2):
    lower = np.array(hsv_256(colorVal1))
    upper = np.array(hsv_256(colorVal2))
    return cv2.inRange(frame, lower, upper)

        