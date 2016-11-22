import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import math
from bluedetection import bluest, redAndGreenDetection, transform, findCorners
from robotdetection import detectRobot
import picamera
from picamera.array import PiRGBArray
from pathfinding2 import findPath
from generatemap import generateMap, mapToImage

def init_camera():
    camera = picamera.PiCamera()
    camera.resolution = (1600, 1200)
    return camera

def capture_image(camera):
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array
    return img


if __name__ == '__main__':
    
#    camera = init_camera()
    camera = init_camera()
    img = capture_image(camera)

    corners = findCorners(img)
    img = transform(img, corners)
#    img = cv2.GaussianBlur(img, 

    robotStart = time.time()
    (img, pos, ang, diam) = detectRobot(img)
    robotEnd = time.time()
    print("Robot detection duration: {}".format(robotEnd - robotStart))
    
    smallPos = (int(pos[0] / 20), int(pos[1] / 20))
    mapStart = time.time()
    m = generateMap(img, diam/40)
    mapEnd = time.time()
    print("Map generation duration: {}".format(mapEnd - mapStart))

    pathStart = time.time()
    path = findPath(m, smallPos, (70, 10), int(diam/40))
    pathEnd = time.time()
    print("Path finding duration: {}".format(pathEnd - pathStart))
    for p in path:
        m[p[0]][p[1]] = 2
    mapToImage(m, len(m), len(m[0]))
