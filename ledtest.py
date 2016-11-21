import picamera
from picamera.array import PiRGBArray
from time import sleep
import cv2
import matplotlib.pyplot as plt


camera = picamera.PiCamera()
##camera.shutter_speed=1500
camera.start_preview()
sleep(3)
camera.stop_preview()
rawCapture = PiRGBArray(camera)
camera.capture(rawCapture, format="bgr")
img = rawCapture.array
#cv2.imwrite('/home/pi/best_course.png', img)

##img = cv2.imread('/home/pi/green_test.png')
##plt.imshow(img)
##plt.show()
##for x in range(278,279):
##    for y in range(349,354):
##        val = img[y,x]
##        print("{}".format(val))
            
