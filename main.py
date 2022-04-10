from cv2 import COLOR_BGR2GRAY
import numpy as np
import cv2
from helper import hsv_256,mask_makr,average
import time
# detects coke can
# it works woo

# object detector color parameters in HSV
primary_apex = [0, 40, 50]
primary_vortex = [30, 100, 100]
secondary_apex = [330, 40, 50]
secondary_vortex = [360, 100, 100]
outputfolder = "coke_dataset/"
obj_width = 300
obj_height = 300

cap = cv2.VideoCapture(0)
width = int(cap.get(3))
height = int(cap.get(4))
contrast = np.zeros((obj_width, obj_height), np.uint8)
contrast[:][:] = 255
objw, objh = contrast.shape

iterator = 0

while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = mask_makr(hsv, primary_apex, primary_vortex)

    if (secondary_apex is not None):
        mask2 = mask_makr(hsv, secondary_apex, secondary_vortex)
        mask = cv2.bitwise_or(mask, mask2)

    mask_sum = 0
    height_count = 0
    width_count = 0
    height_sum = 0
    width_sum = 0

    for i in range(height):
        for j in range(width):
            maskpix = mask[i][j]
            if (maskpix > 0):
                mask_sum += maskpix
                height_count += 1
                width_count += 1
                height_sum += i
                width_sum += j

    if (mask_sum > 300000):
        cv2.imwrite(outputfolder + str(iterator) + ".jpg", frame)
        iterator += 1
    print(mask_sum)
                
    average_height = average(height_sum, height_count)
    average_width = average(width_sum, width_count)
    print(str(average_height) + " " + str(average_width))
    corner1 = (average_width - width//2, average_height - height//2)
    corner2 = (average_width + width//2, average_height + height//2)

    if (corner1[0] < 0):
        corner1[0] = 0
    if (corner1[1] < 0):
        corner1[1] = 0

    if (corner2[0] >= width):
        corner2[0] = width - 1
    if (corner2[1] > height):
        corner2[1] = height - 1

    
    
    royalmask = cv2.bitwise_and(frame, frame, mask=mask)

    

    # blackroyal = cv2.cvtColor(royalmask, COLOR_BGR2GRAY)
    # corners = cv2.goodFeaturesToTrack(blackroyal, 20, 0.01, 20)
    # if (corners is not None):
    #     corners = np.int0(corners)
    # else:
    #     corners = np.array([])

    # for corner in corners:
    #     x, y = corner.ravel()
    #     cv2.circle(royalmask, (x,y), 5, (255,255,255), -1)

    cv2.imshow('sodas', royalmask)
    time.sleep(0.2)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()