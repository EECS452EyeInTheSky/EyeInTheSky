import cv2
import numpy as np
import matplotlib.pyplot as plt
from bluedetection import redest, greenest, bluest, transform
import picamera
import math
from picamera.array import PiRGBArray
from time import sleep
from generatemap import generateMap
from generatemap import mapToImage
#from robotdetection import pos, ang

paths = [ [] ]
pathI = 0

SLOPE_FOR_ZERO_X = 9999999

# Start is position of Robot, Finish is position of target
# For correct navigation, we find a path in "reverse"
# So "start" here becomes "finish" for findNearestObstacle and
#    "finish here becomes "start" for findNearestObstacle
def findPath(m, start, finish, radius):
    findNearestObstacle(m, finish, start, 0, radius)
    bestPath = pickBestPath(finish, start)
    print ("The best path is: {}".format(bestPath))
    mapToImage(m, 80, 60)
    return bestPath

def findNearestObstacle(m, start, finish, numOfCollisions, radius):
    global pathI
    global paths

    Mx = len(m)
    My = len(m[0])
    
    (fx, fy) = finish
##    print("Finish is {}".format(finish))
    (sx, sy) = start
    if fx == sx:
        slope = SLOPE_FOR_ZERO_X
    else:
        slope = abs((fy - sy) / (fx - sx))
##    print ("The slope is {}".format(slope))
    (cx, cy) = start
    hitObstacle = False
    hitFinish = False
    while not hitObstacle and not hitFinish:
        if fx == cx:
            newSlope = SLOPE_FOR_ZERO_X
        else:
            newSlope = abs((fy - cy) / (fx - cx))
##        print("The newSlope is {}".format(newSlope))
        if (newSlope < slope):
            incX = int((fx - cx) / abs(fx - cx))
            incY = int(0)
        else:
            incX = int(0)
            incY = int((fy - cy) / abs(fy - cy))
        cx = int(cx + incX)
        cy = int(cy + incY)
        sensors = getSensors(m, cx, cy, radius)
##        if cx - radius < 0 or cx + radius > Mx:
##            hitObstacle = True
##        if cy - radius < 0 or cy + radius > My:
##            hitObstacle = True
##        if not hitObstacle:
##            sensors = [
##                m[cx-radius][cy-radius],
##                m[cx][cy-radius],
##                m[cx+radius][cy-radius],
##                m[cx+radius][cy]  ,
##                m[cx+radius][cy+radius]  ,
##                m[cx][cy+radius],
##                m[cx-radius][cy+radius],
##                m[cx-radius][cy]
##            ]
        
        print("Cx is {}. Cy is {}".format(cx, cy))
        if cx == fx and cy == fy:
            hitFinish = True
##        if m[cx][cy] == 1:
##            hitObstacle = True
        Angle = math.atan2(fy-cy, fx-cx)
        Angle = math.degrees(Angle)
        if Angle < 0:
            Angle = Angle + 360
            
        if not hitObstacle and not hitFinish:
            if (Angle >= 337.5 or Angle < 22.5) and  (sensors[2]==1 or sensors[3]==1 or sensors[4]==1):
                hitObstacle = True 
            elif  (Angle >= 22.5 and Angle < 67.5) and (sensors[1]==1 or sensors[2]==1 or sensors[3]==1):
                hitObstacle = True
            elif (Angle >= 67.5 and Angle < 112.5) and (sensors[0]==1 or sensors[1]==1 or sensors[2]==1):
                hitObstacle = True
            elif (Angle >= 112.5 and Angle < 157.5) and (sensors[7]==1 or sensors[0]==1 or sensors[1]==1):
                hitObstacle = True
            elif (Angle >= 157.5 and Angle < 202.5) and (sensors[6]==0 or sensors[7]==0 or sensors[0]==0):
                hitObstacle = false
            elif (Angle >= 202.5 and Angle < 247.5) and (sensors[5]==1 or sensors[6]==1 or sensors[7]==1):
                hitObstacle = True
            elif (Angle >= 247.5 and Angle < 292.5) and (sensors[4]==1 or sensors[5]==1 or sensors[6]==1):
                hitObstacle = True
            elif (Angle >= 292.5 and Angle < 337.5) and (sensors[3]==1 or sensors[4]==1 or sensors[5]==1):
                hitObstacle = True
                
##        if not hitFinish and hitObstacle:
##            cx = cx - incX
##            cy = cy - incY
        if m[cx][cy] == 0:
            m[cx][cy] = 2
##    print('pos = {} {}'.format(cx, cy))
    #mapToImage(m, 80, 60)  
    #points.append((cx, cy))
    if hitObstacle and not hitFinish:
        print("Hit obstacle at {}, {}. Collision count is {}".format(cx, cy, numOfCollisions))
        sleep(3)
        (rx, ry) = findRightCorner(m, (cx, cy), finish, radius)
        (lx, ly) = findLeftCorner(m, (cx, cy), finish, radius)
        paths[pathI].append((rx, ry))
        if rx != -1:
            findNearestObstacle(m, (rx, ry), finish, numOfCollisions+1, radius)
        pathI += 1
        #paths[pathI] = paths[pathI-1][:numOfCollisions]
        paths.append(paths[pathI-1][:numOfCollisions])
        paths[pathI].append((lx, ly))
        if lx != -1:
            findNearestObstacle(m, (lx, ly), finish, numOfCollisions+1, radius)
            #pathI += 1
            #paths[pathI] = paths[pathI-1][:numOfCollisions]
            #paths.append(paths[pathI-1][:numOfCollisions])
def rotateRight(sensors):
    prev = 0
    for i in range(len(sensors)):
        if sensors[i] != 1 and prev == 1:
            return (i+1) % 2 + i + 1
        else:
            prev = sensors[i]
    return 2

def rotateLeft(sensors):
    prev = 0
    i = 7
    while(i>0):
        if sensors[i] != 1 and prev == 1:
            return i + i % 2
        else:
            prev = sensors[i]
            i = i - 1
        #print ("i is {}".format(i))
    return 8

def getSensors(m, cx, cy, radius=1):
    Mx = len(m)
    My = len(m[0])
    s = [0,0,0,0,0,0,0,0]
##    print('cx = {}'.format(cx))
##    print('cy = {}'.format(cy))
##    print('radius = {}'.format(radius))
    #out of bounds = obstacle
    if cx - radius < 0:
        s[0] = s[7] = s[6] = 1
    if cx + radius >= Mx:
        s[2] = s[3] = s[4] = 1
    if cy - radius < 0:
        s[0] = s[1] = s[2] = 1
    if cy + radius >= My:
        s[4] = s[5] = s[6] = 1
    print('s0 = {}'.format(s))

        #012
        #7 3
        #654
    #define sensors
    if s[0] == 0:
        s[0] = m[cx-radius][cy-radius]
    if s[1] == 0:
        s[1] = m[cx][cy-radius]
    if s[2] == 0:
        s[2] = m[cx+radius][cy-radius]
    if s[3] == 0:
        s[3] = m[cx+radius][cy]
    if s[4] == 0:
        s[4] = m[cx+radius][cy+radius]
    if s[5] == 0:
        s[5] = m[cx][cy+radius]
    if s[6] == 0:
        s[6] = m[cx-radius][cy+radius]
    if s[7] == 0:
        s[7] = m[cx-radius][cy]
    print('s = {}'.format(s))
    return s
    
    
def findRightCorner(m, start, finish, radius=1):
#0 1 2
#7   3
#6 5 4
    (fx, fy) = finish
    (sx, sy) = start
    (cx, cy) = start
    while True:
        if m[cx][cy] == 0:
            m[cx][cy] = 2
        sensors = getSensors(m, cx, cy, radius)
##        sensors = [
##            m[cx-radius][cy-radius],
##            m[cx][cy-radius],
##            m[cx+radius][cy-radius],
##            m[cx+radius][cy]  ,
##            m[cx+radius][cy+radius]  ,
##            m[cx][cy+radius],
##            m[cx-radius][cy+radius],
##            m[cx-radius][cy]
##        ]
        if   (fy < cy and fx > cx):
            check = [ 1, 2, 3]
        elif (fy < cy and fx < cx):
            check = [ 0, 1, 7 ]
        elif (fy == cy and fx > cx):
            check = [ 3 ]
        elif (fy == cy and fx < cx):
            check = [ 7 ]
        elif (fy > cy and fx > cx):
            check = [ 3, 4, 5 ]
        elif (fy > cy and fx < cx):
            check = [ 7, 6, 5 ]
        elif (fy < cy and fx == cx):
            check = [ 1 ]
        else:
            check = [ 5 ]

        hit = False
        for c in check:
            if sensors[c] == 1:
                hit = True  
        if not hit:
            return (cx, cy)
        direction = rotateRight(sensors)
        if direction == 2:
            cy -= 1
        elif direction == 4:
            cx += 1
        elif direction == 6:
            cy += 1
        else:
            cx -= 1
      
    
def findLeftCorner(m, start, finish, radius=1):
#0 1 2
#7   3
#6 5 4
    (fx, fy) = finish
    (sx, sy) = start
    (cx, cy) = start
    while True:
        if m[cx][cy] == 0:
            m[cx][cy] = 2
        #m[cx][cy] = 2
##        print ("The current position is ({}, {})".format(cx, cy))
        sensors = getSensors(m, cx, cy, radius)
##        sensors = [
##            m[cx-radius][cy-radius],
##            m[cx][cy-radius],
##            m[cx+radius][cy-radius],
##            m[cx+radius][cy]  ,
##            m[cx+radius][cy+radius]  ,
##            m[cx][cy+radius],
##            m[cx-radius][cy+radius],
##            m[cx-radius][cy]
##        ]

        if   (fy < cy and fx > cx):
            check = [ 1, 2, 3]
        elif (fy < cy and fx < cx):
            check = [ 0, 1, 7 ]
        elif (fy == cy and fx > cx):
            check = [ 3 ]
        elif (fy == cy and fx < cx):
            check = [ 7 ]
        elif (fy > cy and fx > cx):
            check = [ 3, 4, 5 ]
        elif (fy > cy and fx < cx):
            check = [ 7, 6, 5 ]
        elif (fy < cy and fx == cx):
            check = [ 1 ]
        else:
            check = [ 5 ]

        hit = False
        for c in check:
            if sensors[c] == 1:
                hit = True  
        if not hit:
            return (cx, cy)
        direction = rotateLeft(sensors)
        if direction == 2:
            print ("Moving up")
            cy -= 1
        elif direction == 4:
            print ("Moving right")
            cx += 1
        elif direction == 6:
            print ("Moving down")
            cy += 1
        else:
            print ("Moving left")
            cx -= 1
            
def pickBestPath(start, finish):
    lowestDist = 9999999
    for path in paths:
        i = 1
        dist = 0
        nPath = [start] + path + [finish]
        for i in range(len(nPath)):
            (sx, sy) = nPath[i-1]
            (fx, fy) = nPath[i]
            dist = dist + math.sqrt((sx-fx) ** 2 + (sy-fy) ** 2)
##        if len(path) == 0:
##            return path
##        elif len(path) == 1:
##            dist = dist + math.sqrt((start[0] - finish[0]) ** 2 + (start[1] - finish[1]) ** 2)
##        else:
##            dist += math.sqrt((path[0][0] - finish[0]) ** 2 + (path[0][1] - finish[1]) ** 2)
##            dist += math.sqrt((path[-1][0] - start[0]) ** 2 + (path[-1][1] - start[1]) ** 2)
        if lowestDist > dist:
#            print ("New best path: {}".format(path))
#            print ("Total distance: {}".format(dist))
            lowestDist = dist
            bestPath = path
    return bestPath
