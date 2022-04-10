import numpy as np
import cv2

def hsv_256(hsv100):
    hsv256 = []
    hsv256.append(int(hsv100[0] * 255 / 360))
    hsv256.append(int(hsv100[1] * 255 / 100))
    hsv256.append(int(hsv100[2] * 255 / 100))

    return hsv256

def mask_makr(frame, colorVal1, colorVal2):
    lower = np.array(hsv_256(colorVal1))
    upper = np.array(hsv_256(colorVal2))
    return cv2.inRange(frame, lower, upper)

def average(sum, iterations):
    if (iterations == 0):
        return 0
    return int(sum/iterations)
