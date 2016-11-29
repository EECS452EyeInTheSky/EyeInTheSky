import picamera
from picamera.array import PiRGBArray
from time import sleep
import cv2
import matplotlib.pyplot as plt


camera = picamera.PiCamera()
#camera.capture('/home/pi/green_test.png')
#exit()
##camera.shutter_speed=1500
camera.start_preview()
sleep(2)
camera.stop_preview()
#exit()
#camera.stop_preview()
rawCapture = PiRGBArray(camera)
camera.capture(rawCapture, format="bgr")
img = rawCapture.array
cv2.imwrite('/home/pi/yellow_test.png', img)
exit()
####img = cv2.imread('/home/pi/green_test.png')
##plt.imshow(img)
##plt.show()
##for x in range(590, 600):
##    for y in range(590, 600):
##        val = img[y,x]
##        print("{}".format(val))
            
