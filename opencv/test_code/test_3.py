import cv2
import numpy as np
print("OpenCV version : {0}".format(cv2.__version__))
major_ver, minor_ver, subminor_ver = (cv2.__version__).split('.')
print("Major version : {0}".format(major_ver))
print("Minor version : {0}".format(minor_ver))
print("Subminor version : {0}".format(subminor_ver))


image = cv2.imread("color_wheel.jpeg")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
mask = cv2.inRange(hsv, lower_red, upper_red)

cv2.imshow("Original Image", image)
cv2.imshow("HSV", hsv)
cv2.imshow("Detected Red", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()