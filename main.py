from cv2 import COLOR_BGR2GRAY
import numpy as np
import cv2
from helper import hsv_256,mask_makr,average
from soda_hsv import soda_dictionary
import time
# detects coke can
# it works wooo

# object detector color parameters in HSV
desired_soda = "background" #input soda type
soda_index = soda_dictionary[desired_soda]
outputfolder = f"sodas/{desired_soda}_dataset/" # output folder
obj_width = 300 # exists in case I want to implement a hard obj size
obj_height = 300 # exists in case I want to implement a hard obj size
export_size = 50 # export height and width in pixels
sens = 0 # scale 1-30, higher is less sensitive, 5 is pretty good, set to 0 to take any


cap = cv2.VideoCapture(0)
width = int(cap.get(3)) # grabs video width
height = int(cap.get(4)) # grabs video height
contrast = np.zeros((obj_width, obj_height), np.uint8) # creates a white background for object mask in case I want it
contrast[:][:] = 255 # sets contrast to all white
primary_vortex = soda_index[0] # lower bound of color
primary_apex = soda_index[1] # upper bound of color
secondary_vortex = None # possible second lower bound of color
secondary_apex = None # possible second upper bound of color
if (len(soda_index) > 2):
    secondary_vortex = soda_index[2]
    secondary_apex = soda_index[3]

iterator = 0 # keeps track of number of frames created

while True:
    ret, frame = cap.read() # turns into RGB value

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = mask_makr(hsv, primary_vortex, primary_apex)

    if (secondary_apex is not None):
        mask2 = mask_makr(hsv, secondary_vortex, secondary_apex)
        mask = cv2.bitwise_or(mask, mask2)

    mask_sum = 0 # determines mask density
    mask_count = 0 # determines how many pixels are masked
    height_sum = 0 # determines average height for mask
    width_sum = 0 # determines average width for mask

    # applies the mask
    for i in range(height):
        for j in range(width):
            maskpix = mask[i][j]
            if (maskpix > 0):
                mask_sum += maskpix
                mask_count += 1
                height_sum += i
                width_sum += j

    # merges mask with color 
    royalmask = cv2.bitwise_and(frame, frame, mask=mask)

    print(mask_sum)
    if (mask_sum >= sens * 100000): # boxes the detected can if found
        quality = True

        average_height = average(height_sum, mask_count)
        average_width = average(width_sum, mask_count)
        print(str(average_height) + " " + str(average_width))

        corner1 = [int(average_width - width/3 * (height/width)), average_height - height//3]
        corner2 = [int(average_width + width/3 * (height/width)), average_height + height//3]

        print(corner1)
        print(corner2)
        print("sledge")
        if (corner1[0] < 0):
            corner1[0] = 0
            quality = False
        if (corner1[1] < 0):
            corner1[1] = 0
            quality = False

        if (corner2[0] >= width):
            corner2[0] = width - 1
            quality = False
        if (corner2[1] > height):
            corner2[1] = height - 1
            quality = False
        
        if (quality):
            print(corner1)
            print(corner2)
            frame_copy = np.copy(frame)
            export_frame = frame_copy[corner1[1]:corner2[1], corner1[0]:corner2[0]]
            print(export_frame.shape)
            cv2.imwrite(outputfolder + str(iterator) + ".jpg", cv2.resize(export_frame, [export_size,export_size]))
            iterator += 1
        
        cv2.rectangle(royalmask, corner1, corner2, (255,255,255), 5)



        
    # add this script back in for corner detection
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
    time.sleep(0.1)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()