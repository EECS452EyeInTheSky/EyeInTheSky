import cv2
import numpy as np
import matplotlib.pyplot as plt
from bluedetection import redest, greenest, bluest, transform, redAndGreenDetection, yellowest
import picamera
import math
from picamera.array import PiRGBArray
from time import sleep
import time
from generatemap import generateMap
from generatemap import mapToImage
#from pathfinding import findPath
from pathfinding2 import findPath
import os
import subprocess
from ctypes import *

#counter = 0;
diam = 0

class Point(Structure):
   _fields_ = [("x", c_uint), ("y", c_uint)] 

class Pixel(Structure):
    _fields_ = [("b", c_ubyte), ("g", c_ubyte), ("r", c_ubyte)]


c_module = cdll.LoadLibrary('./c/test.so')
c_module.c_redest.restype = Point
c_module.c_greenest.restype = Point
c_module.c_yellowest.restype = Point

class Formatter(object):
    def __init__(self, im):
        self.im = im
    def __call__(self,x,y):
        z = self.im.get_array()[int(y), int(x)]
        return 'x={:.01f}, y={:,01f, z={:,01f}'.format(x, y, z)
    
def detectRobot(img, y_low=0, y_high=None, x_low=0, x_high=None):
   # img = cv2.imread('robot.jpg')
##    img = cv2.GaussianBlur(img, (5,5), 0)

    if y_high == None:
        y_high, _, _ = img.shape
    if x_high == None:
        _, x_high, _ = img.shape
#    height, width, channels = img.shape

#    dummy = redest(img, 0, height, 0, width)
#
#    start = time.time()
#    r_pt = redest(img, 0, height, 0, width)
#    g_pt = greenest(img, 0, height, 0, width)
#    end = time.time()
#    print("Total duration (old): {}".format(end - start))

#    (r_pt, g_pt) = redAndGreenDetection(img, 0, height, 0, width)

    #(r_pt, g_pt) = redAndGreenDetection(img, y_low, y_high, x_low, x_high)
    r_pt = c_module.c_redest(img.ctypes.data_as(POINTER(c_ubyte)), 0, y_high, 0, x_high)
    g_pt = c_module.c_greenest(img.ctypes.data_as(POINTER(c_ubyte)), 0, y_high, 0, x_high)
    r_pt = (r_pt.x, r_pt.y)
    g_pt = (g_pt.x, g_pt.y)
    
    print("Green point is at: {}".format(g_pt))
    print("Red Point is at: {}".format(r_pt))
    pos = ((g_pt[0] + r_pt[0]) / 2, (g_pt[1] + r_pt[1]) / 2)
    diam = math.sqrt((g_pt[0]-r_pt[0])**2 + (g_pt[1]-r_pt[1])**2) * 2.5
    if g_pt[0] == r_pt[0]:
        ang = 0
    else:
        ang = math.atan2((g_pt[1]-r_pt[1]),(g_pt[0]-r_pt[0]))
        ang = 180 * ang / math.pi
    #plt.imshow(img)
    #plt.show()
    #img = removeRobot(img, g_pt, r_pt, pos)
    img = removeRobotCircle(img, g_pt, r_pt, pos)
    return (img, pos, ang, diam)

def detectTarget(img, y_low=0, y_high = None, x_low=0, x_high=None):
    if y_high == None:
        y_high, _, _ = img.shape
    if x_high == None:
        _, x_high, _ = img.shape
    #target = yellowest(img, y_low, y_high, x_low, x_high)
    raw_target = c_module.c_yellowest(img.ctypes.data_as(POINTER(c_ubyte)), 0, y_high, 0, x_high)
#    print("Target is at {}".format(target))
#    plt.imshow(img)
#    plt.show()
    target = (raw_target.x, raw_target.y)
    global diam
##    while diam==0:
##        sleep(0.1)
    cv2.circle(img, target, int(diam/2), [0, 0, 0], cv2.FILLED)
    return (img, target)

def removeRobot(img, g_pt, r_pt, pos):
    start = time.time()
    global diam
#    diam = math.sqrt((g_pt[0]-r_pt[0])**2 + (g_pt[1]-r_pt[1])**2) * 1.5
    #print(diam)
    x_low =int(pos[0] - diam/2)
    x_high = int(pos[0] + diam/2)
    y_low = int(pos[1] - diam/2)
    y_high = int(pos[1] + diam/2)
    print('xlow is ', x_low, 'xhigh is ', x_high, 'ylow is ', y_low, 'yhigh is ', y_high)
    if x_high > img.shape[1]:
        x_high = img.shape[1]
    if x_low < 0:
        x_low = 0
    if y_high > img.shape[0]:
        y_high = img.shape[0]
    if y_low < 0:
        y_low = 0
    for x in range(x_low, x_high):
        for y in range(y_low, y_high):
                img[y,x] = [0, 0, 0]
    #plt.imshow(img)
    #plt.show()
    end = time.time()
#    print("Time to remove robot: {}".format(end - start))
    return img 

def removeRobotCircle(img, g_pt, r_pt, pos):
    start = time.time()

#    if (counter = 0)
#      #os(sudo rfcomm connect /dev/rfcomm0 $MAC)
#      subprocess.check_output('sudo', 'rfcomm', 'connect', '/dev/rfcomm0 $MAC')
#      counter = counter + 1
    global diam
    pos = (int(pos[0]), int(pos[1]))
    diam = math.sqrt((g_pt[0]-r_pt[0])**2 + (g_pt[1]-r_pt[1])**2) * 2.5
    cv2.circle(img, pos, int(diam/2), [0, 0, 0], cv2.FILLED)
    end = time.time()
#    print("Time to remove robot: {}".format(end - start))
    return img
    
if __name__ == '__main__':
#    fig, ax = plt.subplots()
    camera = picamera.PiCamera()
    camera.resolution = (1600, 1200)
#    camera.start_preview()
#    sleep(60)
#    camera.stop_preview()
#
#    exit()
    
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array
    cv2.imwrite('/home/pi/mat.png', img)
#    img = cv2.imread('/home/pi/best_course.png')
##    print("Raw image")
##    plt.imshow(img)
##    plt.show()
    
    start = time.time()
    img = transform(img)
#    print("Transformed image")
#    im = ax.imshow(img, interpolation='none')
#    ax.format_coord = Formatter(im)
#    plt.imshow(img)
#    plt.show()
    img = cv2.GaussianBlur(img, (11,11), 0)

    robotStart = time.time()
    (img, pos, ang, diam) = detectRobot(img)
    robotEnd = time.time()
    print("Robot detection duration: {}".format(robotEnd - robotStart))
    
    # Not cool. Change later
    pos = (int(pos[0] / 20), int(pos[1] / 20))
    mapStart = time.time()
    m = generateMap(img, diam/2)
    mapEnd = time.time()
    print("Map generation duration: {}".format(mapEnd - mapStart))
    # Seriously not cool
    
    print ("The robot's center is at {} with diameter of {}".format(pos, diam))
    #print("The size of m is {}".format(len(m)), len(m[0]))
    pathStart = time.time()
    path = findPath(m, pos, (70, 10), int(diam/40))
    pathEnd = time.time()
    print("Path finding total duration: {}".format(pathEnd - pathStart))
    end = time.time()
    print("Total duration for whole thing: {}".format(end - start))
    for p in path:
        m[p[0]][p[1]] = 2
        
    mapToImage(m, len(m), len(m[0]))


    #  custom control of robot
   
##    (r2, g2) = redAndGreenDetection(img, y_low, y_high, x_low, x_high)
##    
##    print("Green point is at: {}".format(g2))
##    print("Red Point is at: {}".format(r2))
##    pos = ((g2[0] + r2[0]) / 2, (g2[1] + r2[1]) / 2)
    
##    (_, curr_pos, curr_ang,_) = detectRobot(img) 
##    #output next position
##    for p in path
##       #if((m[p[0]][p[1]]) == 2)
##         next_pos[0] = p[0]
##         next_pos[1] = p[1]
##         (_, curr_pos, curr_ang,_) = detectRobot(img)
##         if next_pos[0] == r_pt[0]:
##           next_angle = 0
##          else:
##           next_angle = math.atan((g_pt[1]-r_pt[1])/(g_pt[0]-r_pt[0]))
##         if((next_pos[1]!=curr_pos[1]) && (next_pos[0]!=curr_pos[0]):
##          while(next_angle!=curr_angle)
##               if((next_ang-curr_ang)<0):
##                  subprocess.check_output('echo', '\'r\'', '/dev/rfcomm0\')
##                  sleep(0.1)
##               elif((next_ang-curr_ang)>0):
##                  subprocess.check_output('echo', ''l'', '/dev/rfcomm0\')
##                  sleep(0.1)
##          subprocess.check_output('echo', ''F'', '/dev/rfcomm0\')
##          (_, curr_pos, curr_ang,_) = detectRobot(img)
##          sleep(0.1)
##
##
##    #next pos and next ang
##
##    # do changes in the position 
##
##    #(_, curr_pos, curr_ang,_) = detectRobot(img)
##    #compare current position with the actual position
##    #(_, next_pos, next_ang,_) = detectRobot(img)
####    if((next_pos[1]!=curr_pos[1]) && (next_pos[0]!=curr_pos[0]):
####          while(next_angle!=curr_angle)
####               if((next_ang-curr_ang)<0):
####                  subprocess.check_output('echo', '\'r\'', '/dev/rfcomm0\')
####                  sleep(0.1)
####               elif((next_ang-curr_ang)>0):
####                  subprocess.check_output('echo', ''l'', '/dev/rfcomm0\')
####                  sleep(0.1)
####          subprocess.check_output('echo', ''F'', '/dev/rfcomm0\')
####          (_, curr_pos, curr_ang,_) = detectRobot(img)
####          sleep(0.1)
##          
####       if(((next_pos[1]-currpos[1])>0) && ((next_pos[0]-currpos[0])>0):
####          if(next_angle == curr_angle)):
####            subprocess.check_output('echo', ''B'', '/dev/rfcomm0\')
####            sleep(0.1)
####          elif(next_angle - curr_angle = 180):
####            subprocess.check_output('echo', ''F'', '/dev/rfcomm0\')
####            sleep(0.1)
##       
##
##       
####          subprocess.check_output('echo', ''r'', '/dev/rfcomm0\')
####          sleep(0.2)
##          
##
##    
####    if (next_pos != curr_pos):
####       if((next_pos[1]-currpos[1])>0):
####          while(next_pos[1]!=curr_pos[1])
####            if(next_ang!=curr_ang):
####              if((next_ang-curr_ang)<0):
##                  subprocess.check_output('echo', '\'r\'', '/dev/rfcomm0\')
####               sleep(0.1)
####              else:
####               subprocess.check_output('echo', ''a'', '/dev/rfcomm0\')
####               sleep(0.1)
####            elif ((next_pos!=curr_pos) && (next_angle == curr_angle)):
####               subprocess.check_output('echo', ''w'', '/dev/rfcomm0\')
####               sleep(0.1)
####            elif ((next_pos!=curr_pos) && (next_angle - curr_angle = 180)):
####               subprocess.check_output('echo', ''s'', '/dev/rfcomm0\')
####               sleep(0.1)
##             
##          # d = right turn, a = left turn   w go forward   s go backward
##          # using another keyboard "game keys" for robot movement
##
##
##    #connect to hc 06 module
##    #echo 'F' > /dev/rfcomm0\
##    (_, pos, ang,_) = detectRobot(img)
##    subprocess.check_output('echo', ''F'', '/dev/rfcomm0\')
    
    
    #print("The path is: {}".format(path))
###low_red = np.array([0, 0, 90])
###upper_red = np.array([80, 80, 255])
###mask = cv2.inRange(img, low_red, upper_red)
###mask = cv2.dilate(mask, None, iterations=1)
###masked_img = cv2.bitwise_and(img, img, mask=mask)
##masked_img = cv2.GaussianBlur(masked_img, (5,5), 0)
##ret, masked_img = cv2.threshold(masked_img, 25, 255, cv2.THRESH_BINARY)
##
##plt.imshow(masked_img)
##plt.show()
##params = cv2.SimpleBlobDetector_Params()
##params.filterByArea = True
##params.minDistBetweenBlobs = 0
##params.minArea = 10
##params.filterByCircularity = False
##params.minCircularity = 0.1
##params.maxCircularity = 1.0
##params.filterByInertia = False
##params.filterByConvexity = False
##detector = cv2.SimpleBlobDetector_create(params)
##keypoints = detector.detect(masked_img)
##print(keypoints)
##for p in keypoints:
##    x = p.pt[0]
##    y = p.pt[1]
##    print("Keypoint at ({},{})".format(x, y))
##plt.imshow(masked_img)
##plt.show()
##img_gray = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
##plt.imshow(img_gray)
##plt.show()
##ret, thresh = cv2.threshold(img_gray, 50, 255, 0)
##_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
###print(contours)
##cv2.drawContours(thresh, contours, -1, (0,255,0), 3)
##plt.imshow(thresh)
##plt.show()
