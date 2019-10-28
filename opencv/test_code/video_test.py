import cv2
import numpy as np
import sys
import time

#Takes in video and return the frame at which the light turns on
def is_light_on(video_cap):
    # HSV range for white light
    white_lower = np.array([0, 0, 20])
    white_upper = np.array([5, 2, 255])
    frame_count = 0
    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            frame_count += 1
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, white_lower, white_upper)
            count = cv2.countNonZero(mask)
            #light is on
            if count > 100000 and count < 180000:
                return frame_count
                #print("light is on")
                # print(frame_count)
                # print(count)
            #else:
                #print("light is off")
            # Display the resulting frame
            #resized_hsv = cv2.resize(hsv, (0,0), fx=0.25, fy=0.25)
            #resized_mask = cv2.resize(mask, (0,0), fx=0.25, fy=0.25)
            #resized_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            #cv2.imshow('Frame', resized_frame)
            #cv2.waitKey(100)
            # Press Q on keyboard to  exit
            #if cv2.waitKey(25) & 0xFF == ord('q'):
            #    break
            # Break the loop
        else:
            return -1

print("OpenCV version : {0}".format(cv2.__version__))
major_ver, minor_ver, subminor_ver = (cv2.__version__).split('.')
print("Major version : {0}".format(major_ver))
print("Minor version : {0}".format(minor_ver))
print("Subminor version : {0}".format(subminor_ver))

cap = cv2.VideoCapture("floodlight_outside.mp4")
if cap.isOpened() == False:
    print("Error: cap.isOpened()")
    sys.exit()
print(is_light_on(cap))
# When everything done, release the video capture object
cap.release()
cv2.destroyAllWindows()
