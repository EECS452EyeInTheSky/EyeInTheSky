import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import math
from bluedetection import bluest, redAndGreenDetection, transform, findCorners, yellowest
from robotdetection import detectRobot, detectTarget
import picamera
from picamera.array import PiRGBArray
from pathfinding2 import findPath
from generatemap import generateMap, mapToImage
import threading

curPos = None
curAng = None
curCorners = None
curCamera = None
curImage = None
curDiam = None

#targetPoint = (70, 50)
#targetPoint = (40, 40)
targetPos = None
targetAng = 0
targetPath = None
targetPos = None
counter = 0
f = None
b = []
def init_camera():
    camera = picamera.PiCamera()
    camera.resolution = (1600, 1200)
    return camera

def capture_image(camera):
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array
    return img



##def targetpath():
##    if (counter == 0):
##        time.sleep(1)
##        camera = init_camera()
##        img = capture_image(camera)
##
##        corners = findCorners(img)
##        img = transform(img, corners)
##    #    img = cv2.GaussianBlur(img, 
##
##        robotStart = time.time()
##        (img, pos, ang, diam) = detectRobot(img)
##        robotEnd = time.time()
##        print("Robot detection duration: {}".format(robotEnd - robotStart))
##        
##        smallPos = (int(pos[0] / 20), int(pos[1] / 20))
##        mapStart = time.time()
##        m = generateMap(img, diam/40)
##        mapEnd = time.time()
##        print("Map generation duration: {}".format(mapEnd - mapStart))
##
##        pathStart = time.time()
##        path = findPath(m, smallPos, (70, 10), int(diam/40))
##        pathEnd = time.time()
##        print("Path finding duration: {}".format(pathEnd - pathStart))
##        for p in path:
##            m[p[0]][p[1]] = 2
##        mapToImage(m, len(m), len(m[0]))
##        time.sleep(3)



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

def showImage():
    global curImage
    while curImage == None:
        time.sleep(1)
    while True:
        plt.imshow(curImage)
        plt.show()

def moveTurn():
    global curAng
    global targetAng

    global curPos
    global targetPos
   
    diffAng = curAng - targetAng 
    if diffAng > 180:
        diffAng = diffAng - 360
    if diffAng < -180:
        diffAng = diffAng + 360
    while abs(diffAng) >= 30 and (abs(curPos[0]-targetPos[0]) >= 2 or abs(curPos[1]-targetPos[1]) >= 2): #or diffAng <= -10):
#        print("Current Ang: {}".format(curAng))
#        print("Target Ang: {}".format(targetAng))
#        print("Diff Ang: {}".format(diffAng))
#        print("Current Position: {}".format(curPos))
#        print("Target Position: {}".format(targetPos))
        if (diffAng < 0):
            moveRobot('R')
            time.sleep(0.07)
            moveRobot('S')
        else:
            moveRobot('L')
            time.sleep(0.07)
            moveRobot('S') 
        time.sleep(0.03)
        diffAng = curAng - targetAng 
        if diffAng > 180:
            diffAng = diffAng - 360
        if diffAng < -180:
            diffAng = diffAng + 360

def moveRobotForward():
      global curPos
      global targetAng
      global targetPath
      global curAng
      global targetPos
      angleUpdateTime = 1
    #while (True):
##    camera = init_camera()
##    img = capture_image(camera)
##
##    corners = findCorners(img)
##    img = transform(img, corners)
###    img = cv2.GaussianBlur(img, 
##
##    robotStart = time.time()
##    (img, pos, ang, diam) = detectRobot(img)
##    robotEnd = time.time()
##    print("Robot detection duration: {}".format(robotEnd - robotStart))
##    
##    smallPos = (int(pos[0] / 20), int(pos[1] / 20))
##    mapStart = time.time()
##    m = generateMap(img, diam/40)
##    mapEnd = time.time()
##    print("Map generation duration: {}".format(mapEnd - mapStart))
##
##    pathStart = time.time()
##    path = findPath(m, smallPos, (70, 10), int(diam/40))
##    pathEnd = time.time()
##    print("Path finding duration: {}".format(pathEnd - pathStart))
##    for p in path:
##        m[p[0]][p[1]] = 2
##    mapToImage(m, len(m), len(m[0]))
    
      
      #path2 = path2[::-1]
      while (targetPath == None):
          time.sleep(1.0)
      print("Desired path: {}".format(targetPath))
      p = targetPath[0]
      targetPath = targetPath[1:]
      while p != None:
      #for a in targetPath:
             targetPos = (p[0], p[1])
           #  curPos = (curPos[0] / 20, curPos[1] / 20)
           #if (m[a[0]][a[1]] == 2):
           #  del b[:]
           #  b.append(a[0]*20)
           #  b.append(a[1]*20)
             #a = a*20
#             targetAng = math.atan2(targetPos[1]-curPos[1], targetPos[0]-curPos[0]) * 180 / math.pi
              
             print("The target angle: {}".format(targetAng))
             print("Desired position: {}".format(targetPos))
             #print("Desired positiona a0: {}".format(b[0]))
             #print("Desired position a1: {}".format(b[1]))

             
             while abs(curPos[0] - targetPos[0]) >= 2 or abs(curPos[1] - targetPos[1]) >= 2: 
#                    print("Current position: {}".format(curPos))
#                    print("Target position: {}".format(targetPos))
                    targetAng = math.atan2(targetPos[1]-curPos[1], targetPos[0]-curPos[0]) * 180 / math.pi                  
#                    print("Target angle: {}".format(targetAng))
                    moveRobot('F')
                    moveTurn()
#                    if time.time() - angleUpdateTime > 0.1:
#                        angleUpdateTime = time.time()
#                        moveForwardAngle()
                    time.sleep(0.09)
                    moveRobot('S')
                    time.sleep(0.01)

             #print("*****************************FOUND POINT***********************************")                
                    #moveForwardAngle()
#                moveForwardAngle()
#            moveForwardAngle()
#            time.sleep(0.1)
#            moveRobot('S')
    
#      print("Current position: {}".format(curPos))
             if len(targetPath) > 0:
                p = targetPath[0]
                targetPath = targetPath[1:]
             else:
                p = None

##        while (curPos[0] < 900):
##            targetAng = 0
##            print ("Going to the left")
##            print("Current position: {}".format(curPos))
##            print("Current angle:    {}".format(curAng))
##            moveRobot('F')
##            moveTurn()
###            if time.time() - angleUpdateTime > 0.1:
###                angleUpdateTime = time.time()
###                moveForwardAngle()
##            time.sleep(0.03)
##            moveRobot('S')
##        time.sleep(3)
##        while (curPos[1] < 800):
##            print("Going up")
##            print("Current position: {}".format(curPos))
##            print("Current angle:    {}".format(curAng))
##            moveRobot('F')
##            targetAng = 90
##            moveTurn()
##            #if time.time() - angleUpdateTime > 0.1:
##            #    angleUpdateTime = time.time()
##            #    moveForwardAngle()
##            time.sleep(0.03)
##            moveRobot('S')
##        time.sleep(3)
##        while (curPos[0] > 300):
##            print("Going to the right")
##            print("current position: {}".format(curPos))
##            print("current angle:    {}".format(curAng))
##            moveRobot('F')
##            targetAng = 180
##            moveTurn()
##            #if time.time() - angleupdatetime > 0.1:
##            #    angleupdatetime = time.time()
##            #    moveforwardangle()
##            time.sleep(0.03)
##            moveRobot('S')
##        time.sleep(3)
##        while (curPos[1] > 300):
##            print("Going down")
##            print("Current position: {}".format(curPos))
##            print("Current angle:    {}".format(curAng))
##            moveRobot('F')
##            targetAng = -90
##            moveTurn()
##            #if time.time() - angleUpdateTime > 0.1:
##            #    angleUpdateTime = time.time()
##            #    moveForwardAngle()
##            time.sleep(0.03)
##            moveRobot('S')
##        time.sleep(3)
            
            
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
        
def threadMapping():
    global curPos
    global curImage
    global targetPoint
    global curDiam
    global curImage
    global targetPath

    lastMapTime = 0
    while curDiam == None:
        time.sleep(2)
    #print ("Target point: {}".format(targetPoint))
    while True:
        if time.time() - lastMapTime > 6000:
           mapStart = time.time()
           
           m = generateMap(curImage, curDiam/40)
           #mapToImage(m, len(m), len(m[0]))
           mapEnd = time.time()
           print("Map generation duration: {}".format(mapEnd - mapStart))
           #mapToImage(m, len(m), len(m[0]))
           #targetPoint = yellowest(img, )
           
           targetStart = time.time()
           rawTargetPoint = detectTarget(curImage)
           targetEnd = time.time()
           print("Target detection duration: {}".format(targetEnd - targetStart))

           targetPoint = (int(rawTargetPoint[0]/20), int(rawTargetPoint[1]/20))
           print("The target point: {}".format(targetPoint))

           pathStart = time.time()
           targetPath = findPath(m, curPos, targetPoint, int(curDiam/40))
           pathEnd = time.time()
           print("Path finding duration: {}".format(pathEnd - pathStart))          

           for p in targetPath:
                m[p[0]][p[1]] = 2
           mapToImage(m, len(m), len(m[0]))
            

           lastMapTime = time.time()
        else:
            time.sleep(1)
        

def threadLoop():
    global curCorners
    global curPos
    global curAng
    global curCamera 
    global curImage
    global curDiam

    global targetAng
    global targetPos
    global targetPath
    global targetPoint
##    if(counter == 0):
##        targetpath()
##    else:
    
##    if (curCamera == None):
##        curCamera = init_camera()
    pathTime = 0
    camera = init_camera()
    while True:
        img = capture_image(camera)
        if curCorners == None:
            curCorners = findCorners(img)
	
        img = transform(img, curCorners)
        detectTimeStart = time.time()
        (img, curPos, curAng, curDiam) = detectRobot(img)
        detectTimeEnd = time.time()
#        print("Robot detection took {}".format(detectTimeEnd - detectTimeStart))
        
        curImage = img
        curPos = (int(curPos[0] / 20), int(curPos[1] / 20))
        #if targetPos != None:
        #    targetAng = atan2(targetPos[1]-curPos[1], targetPos[0]-curPos[0]) * 180 / math.pi
#        if time.time() - pathTime >= 5:
#        if targetPath == None:
##            moveRobot('S')
#            smallPos = (int(curPos[0]), int(curPos[1]))
#            mapStart = time.time()
#            m = generateMap(img, curDiam/40)
#            mapEnd = time.time()
#            print("Map generation duration: {}".format(mapEnd - mapStart))
#    
#            pathStart = time.time()
#            targetPath = findPath(m, smallPos, targetPoint, int(curDiam/40))
#            pathEnd = time.time()
#            print("Path finding duration: {}".format(pathEnd - pathStart))
#            #for p in targetPath:
            #    m[p[0]][p[1]] = 2
            #mapToImage(m, len(m), len(m[0])) 
#        time.sleep(0.1)
#    print("The robot's position is: {}".format(curPos))
#    print("The robot's angle is:    {}".format(curAng))
#    print("THe robot's diameter is: {}".format(curDiam))
    
#    threading.Timer(0.1, threadLoop).start()

    

    

if __name__ == '__main__':
    
#    camera = init_camera()


    global targetPoint
    threading.Timer(0, threadLoop).start()
    #threading.Timer(0, showImage).start()
    threading.Timer(0, threadMapping).start()
    moveRobotForward()
    
    while(False):
    
        #if(path != None):
#           time.sleep(1)
           #threadLoop()
        #   threading.Timer(0, threadLoop).start()
        #   print("The robot's position is: {}".format(curPos))
        #   moveRobotForward(path)
        #   print("Outside moverobotforward: {}".format(counter))    
        #print("Completed forward path: {}".format(counter))
        #time.sleep(2)
        
           
        #targetpath()
        #if(path == None):
        if (1 == 0):
            print("Entered path detection")
            camera = init_camera()
            img = capture_image(camera)
            #img = capture_image(curCamera)
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
            path = findPath(m, smallPos, targetPoint, int(diam/40))
            pathEnd = time.time()
            print("Path finding duration: {}".format(pathEnd - pathStart))
            for p in path:
                m[p[0]][p[1]] = 2
            #mapToImage(m, len(m), len(m[0]))
            #counter = counter + 1
            time.sleep(5)
            
     #threadLoop()
    
    
     
