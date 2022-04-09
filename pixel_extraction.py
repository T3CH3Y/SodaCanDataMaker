import numpy as np
import cv2

extractName = "coke.jpg"

def pixel_extraction(extractName):
    extract = cv2.imread(extractName)
    dimensions = extract.shape