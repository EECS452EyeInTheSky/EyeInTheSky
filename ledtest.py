import picamera
from picamera.array import PiRGBArray
from time import sleep
import cv2
import matplotlib.pyplot as plt


camera = picamera.PiCamera()
camera.brightness = 52
camera.framerate = 10
camera.saturation = 100
camera.start_preview()
sleep(1)
camera.stop_preview()
#exit()
camera.capture('/home/pi/yellow_test.png')
exit()
##camera.shutter_speed=1500
camera.start_preview()
sleep(10)
camera.stop_preview()
exit()
rawCapture = PiRGBArray(camera)
camera.capture(rawCapture, format="bgr", use_video_port=True)
img = rawCapture.array
plt.imshow(img)
plt.show()
#cv2.imwrite('/home/pi/red.png', img)
exit()
for i in range(0, 10):
    cv2.imwrite('/home/pi/Project/vid_image_{}.png'.format(i), img)
    sleep(2)
    print("Took image {}".format(i))
exit()
#exit()
#camera.stop_preview()
rawCapture = PiRGBArray(camera)
camera.capture(rawCapture, format="bgr")
img = rawCapture.array
cv2.imwrite('/home/pi/red.png', img)
exit()
####img = cv2.imread('/home/pi/green_test.png')
##plt.imshow(img)
##plt.show()
##for x in range(590, 600):
##    for y in range(590, 600):
##        val = img[y,x]
##        print("{}".format(val))
            
