import cv2
import numpy as np
print("OpenCV version : {0}".format(cv2.__version__))
major_ver, minor_ver, subminor_ver = (cv2.__version__).split('.')
print("Major version : {0}".format(major_ver))
print("Minor version : {0}".format(minor_ver))
print("Subminor version : {0}".format(subminor_ver))

#get image
image = cv2.imread("sunlight.jpg")
#convert image from BGR to HSV to accurately find color
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#HSV color value bounds
lower_yellow = np.array([0, 100, 100])
upper_yellow = np.array([46, 255, 255])
#find area in hsv that match boundes
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
#show images
cv2.imshow("Original Image", image)
cv2.imshow("HSV", hsv)
cv2.imshow("Detected Color", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
