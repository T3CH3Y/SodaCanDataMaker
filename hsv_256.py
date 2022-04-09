import numpy as np
import cv2

def hsv_256(hsv100):
    hsv256 = []
    hsv256.append(int(hsv100[0] * 3.6))
    hsv256.append(int(hsv100[1] * 255 / 100))
    hsv256.append(int(hsv100[2] * 255 / 100))

    return hsv256
