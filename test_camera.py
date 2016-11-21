import picamera
import time

camera = picamera.PiCamera()
camera.resolution = (1600, 1200)
camera.start_preview()
time.sleep(60)
exit()
