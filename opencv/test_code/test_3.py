import cv2
import numpy as np
print("OpenCV version : {0}".format(cv2.__version__))
major_ver, minor_ver, subminor_ver = (cv2.__version__).split('.')
print("Major version : {0}".format(major_ver))
print("Minor version : {0}".format(minor_ver))
print("Subminor version : {0}".format(subminor_ver))

#get image
image = cv2.imread("floodlight_off_outside.jpg")
#convert image from BGR to HSV to accurately find color
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#HSV color value bounds
white_lower = np.array([0, 0, 20])
white_upper = np.array([5, 2, 255])
#find area in hsv that match boundes
mask = cv2.inRange(hsv, white_lower, white_upper)
res = cv2.bitwise_and(image, image, mask= mask)
count = cv2.countNonZero(mask)
print(count)
#show images
resized_image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)
resized_hsv = cv2.resize(hsv, (0,0), fx=0.25, fy=0.25)
resized_mask = cv2.resize(mask, (0,0), fx=0.25, fy=0.25)
resized_res = cv2.resize(res, (0,0), fx=0.25, fy=0.25)
cv2.imshow("Original Image", resized_image)
cv2.imshow("Detected Color", resized_mask)
cv2.imshow("Detected Res", resized_res)

cv2.waitKey(0)
cv2.destroyAllWindows()
