from cv2 import COLOR_BGR2GRAY
import numpy as np
import cv2
from hsv_256 import hsv_256
from mask_makr import mask_makr
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
contrast = np.zeros(obj_width, obj_height, 1), np.uint8)
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

    # denseCord = cv2.matchTemplate(mask, contrast)
    mask_sum = 0
    density_sum = 0
    max_density = 0

    for i in range(height):
        
        for j in range(width):
            mask_sum += mask[i][j]
            if (i + 299 < height and j + 299 < width):
                spaghetti = 0 # FIX ME

            




    royalmask = cv2.bitwise_and(frame, frame, mask=mask)
   

    print(mask_sum)
    if (mask_sum > 300000):
        cv2.imwrite(outputfolder + str(iterator) + ".jpg", frame)
        iterator += 1


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
    time.sleep(3)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()