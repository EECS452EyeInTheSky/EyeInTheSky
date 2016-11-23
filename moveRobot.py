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
import threading

curPos = None
curAng = None
curCorners = None
curCamera = None

targetPos = None
targetAng = 0

f = None

def init_camera():
    camera = picamera.PiCamera()
    camera.resolution = (1600, 1200)
    return camera

def capture_image(camera):
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array
    return img

def moveRobot(c):
    global f
    if f == None or f.close:
        try:
            f = open('/dev/rfcomm0', 'w')
        except Exception as e:
            print("Cannot open file: {}".format(e))
    f.write(c)
    f.flush() 

def moveForwardAngle():
    global curAng
    global targetAng
    
#    diffAng = curAng - targetAng
    diffAng = targetAng - curAng
    print("The diff ang is: {}".format(diffAng))
    if diffAng > 10 or diffAng < -10:
        moveTurn()
#        print("Moving to the right")
#        moveRobot('r')
#    elif diffAng >= 20 and diffAng < 30:
#        print("Moving to the right")
#        moveRobot('r')
#        moveRobot('r')
#    elif diffAng <= -10 and diffAng > -20:
#        print("Moving to the left")
#        moveRobot('l')
#    elif diffAng <= -20 and diffAng > -30:
#        print("Moving to the left")
#        moveRobot('l')
#        moveRobot('l')
#    elif diffAng < -30 or diffAng >= 30:
#        moveTurn()

def moveTurn():
    global curAng
    global targetAng
   
    diffAng = curAng - targetAng 
    if diffAng > 180:
        diffAng = diffAng - 360
    if diffAng < -180:
        diffAng = diffAng + 360
    while (diffAng >= 20 or diffAng <= -20):
        print("The diff ang is (hard turn): {}".format(diffAng))
        if (diffAng < 0):
            moveRobot('R')
            time.sleep(0.05)
            moveRobot('S')
        else:
            moveRobot('L')
            time.sleep(0.05)
            moveRobot('S') 
        time.sleep(0.05)
        diffAng = curAng - targetAng 
        if diffAng > 180:
            diffAng = diffAng - 360
        if diffAng < -180:
            diffAng = diffAng + 360

def moveRobotForward():
    global curPos
    global targetAng
    angleUpdateTime = 1
    while (True):
        while (curPos[0] < 900):
            targetAng = 0
            print ("Going to the left")
            print("Current position: {}".format(curPos))
            print("Current angle:    {}".format(curAng))
            moveRobot('F')
            moveTurn()
#            if time.time() - angleUpdateTime > 0.1:
#                angleUpdateTime = time.time()
#                moveForwardAngle()
            time.sleep(0.03)
            moveRobot('S')
        time.sleep(3)
        while (curPos[1] < 800):
            print("Going up")
            print("Current position: {}".format(curPos))
            print("Current angle:    {}".format(curAng))
            moveRobot('F')
            targetAng = 90
            moveTurn()
            #if time.time() - angleUpdateTime > 0.1:
            #    angleUpdateTime = time.time()
            #    moveForwardAngle()
            time.sleep(0.03)
            moveRobot('S')
        time.sleep(3)
        while (curPos[0] > 300):
            print("Going to the right")
            print("current position: {}".format(curPos))
            print("current angle:    {}".format(curAng))
            moveRobot('F')
            targetAng = 180
            moveTurn()
            #if time.time() - angleupdatetime > 0.1:
            #    angleupdatetime = time.time()
            #    moveforwardangle()
            time.sleep(0.03)
            moveRobot('S')
        time.sleep(3)
        while (curPos[1] > 300):
            print("Going down")
            print("Current position: {}".format(curPos))
            print("Current angle:    {}".format(curAng))
            moveRobot('F')
            targetAng = -90
            moveTurn()
            #if time.time() - angleUpdateTime > 0.1:
            #    angleUpdateTime = time.time()
            #    moveForwardAngle()
            time.sleep(0.03)
            moveRobot('S')
        time.sleep(3)
            
            
#        while (curPos[0] > 200):
#            print("Current position: {}".format(curPos))
#            print("Current angle:    {}".format(curAng))
#            moveRobot('B')
#            if time.time() - angleUpdateTime > 0.3:
#                angleUpdateTime = time.time()
#                moveForwardAngle()
#            moveForwardAngle()
#            time.sleep(0.1)
#            moveRobot('S')
    print("Current position: {}".format(curPos))
        

def threadLoop():
    global curCorners
    global curPos
    global curAng
    global curCamera 

    global targetAng
    global targetPos

    if curCamera == None:
        curCamera = init_camera()
    img = capture_image(curCamera)
    if curCorners == None:
        curCorners = findCorners(img)
    
    img = transform(img, curCorners)   
    (img, curPos, curAng, curDiam) = detectRobot(img)
    if targetPos != None:
        targetAng = atan2(targetPos[1]-curPos[1], targetPos[0]-curPos[0]) * 180 / math.pi
#    print("The robot's position is: {}".format(curPos))
#    print("The robot's angle is:    {}".format(curAng))
#    print("THe robot's diameter is: {}".format(curDiam))
    threading.Timer(0.01, threadLoop).start()
    

if __name__ == '__main__':
    
#    camera = init_camera()
    threadLoop()
    moveRobotForward()
    time.sleep(60)
    exit()



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

