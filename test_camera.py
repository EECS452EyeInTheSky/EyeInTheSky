import picamera
import time
import matplotlib as plt
import cv2

camera = picamera.PiCamera()
camera.resolution = (1600, 1200)
camera.start_preview()
camera.capture('test_image.jpg')
time.sleep(60)
exit()
