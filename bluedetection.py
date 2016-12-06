import cv2
import numpy as np
import matplotlib.pyplot as plt 
import time
import math
from ctypes import *

BLUE   = [255,   0, 0]
RED    = [80,     0, 255]
GREEN  = [90,  150, 0]
YELLOW = [0,   200, 150] 

#def findStrongestColor(img, x_low, x_high, y_low, y_high, color, skipCount=5):
#    x_low = int(x_low)
#    x_high = int(x_high)
#    y_low = int(y_low)
#    y_high = int(y_high)
#    cx = 0
#    cy = 0
#    for x in range(x_low, x_high, skipCount):
#        for y in range(y_low, y_high, skipCount):
#            olda = abs(img[cx, cy] - color)
#            old = olda[0] + olda[1] + olda[2]
#            newa = abs(img[x, y] - color)
#            new = newa[0] + newa[1] + newa[2]
#            if new < old:
#                cx = x
#                cy = y
#    return (cy, cx)
#
#def bluest(img, x_low, x_high, y_low, y_high):
#    color = [255, 0, 0]
#    return findStrongestColor(img, x_low, x_high, y_low, y_high, color, skipCount = 5)

def bluest(img, x_low, x_high, y_low, y_high):
    global BLUE
    print("Searching in range x={} - {} and y={} - {}".format(x_low, x_high, y_low, y_high))
    x_low = int(x_low)
    x_high = int(x_high)
    y_low = int(y_low)
    y_high = int(y_high)
    bluex = 0
    bluey = 0
    old = 9999
    for x in range(x_low, x_high, 2):
         #print(x)
         for y in range(y_low, y_high, 2):

              b, g, r = img[x,y]

              if b>g and b>r:
                 #old = img[bluex,bluey][0]/(1+img[bluex,bluey][0]+img[bluex,bluey][1]+img[bluex,bluey][2])
                 # new = img[x,y][0]/(img[x,y][0]+img[x,y][1]+img[x,y][2]+1)
                 #olda = abs(img[bluex,bluey] - [255,0,0])
                 #old = 2*olda[0]+olda[1]+olda[2]
#                 newa = abs(img[x,y] - [255, 0, 0])
                 newa = abs(img[x, y] - BLUE)
                 new = 2*newa[0]+newa[1]+newa[2]
                 if new < old:
                     old = new
                     bluex = x
                     bluey = y
#    print("Blue detected at: {}".format((bluey, bluex)))
#    print("Blue pixel values: {}".format(img[bluex, bluey]))
                     
    return (bluey, bluex)

def redest(img, x_low, x_high, y_low, y_high):
#print(img.shape)
    count = 0
    x_low = int(x_low)
    x_high = int(x_high)
    y_low = int(y_low)
    y_high = int(y_high)
    redx = 0
    redy = 0
    old = float('inf')
    for x in range(x_low, x_high, 10):
#         print(x)
         for y in range(y_low, y_high, 10):

              b, g, r = img[x,y]
              if r-20>b and r-20>g:
                 count = count + 1
                 #olda = abs(img[redx,redy] - [0,0,255])
                 #old = olda[0]+olda[1]+2*olda[2]
                 newa = abs(img[x,y] - [0, 0, 255])
                 new = newa[0]+newa[1]+2*newa[2]
                 if new < old:
                     old = new
                     redx = x
                     redy = y
#    print("Count is {}".format(count))
    print("red pixel values {}".format(img[redx,redy]))
    return (redy, redx)

def greenest(img, x_low, x_high, y_low, y_high):
#print(img.shape)
    count = 0
    x_low = int(x_low)
    x_high = int(x_high)
    y_low = int(y_low)
    y_high = int(y_high)
    greenx = 0
    greeny = 0
    for x in range(x_low, x_high, 10):
 #        print(x)
         for y in range(y_low, y_high, 10):

              b, g, r = img[x,y]

              if g>b and g>r:
                 count = count + 1
# Old color: 80 200 0
                 olda = abs(img[greenx,greeny] - [80, 200, 0])
#                 olda = abs(img[greenx,greeny] - [80, 200, 0])
                 old = olda[0]+olda[1]+olda[2]
                 newa = abs(img[x,y] - [80, 200, 0])
                 new = newa[0]+newa[1]+newa[2]
                 if new < old:
                     greenx = x
                     greeny = y

#    print("Count is {}".format(count))
    print("green pixel values {}".format(img[greenx,greeny]))
    return (greeny, greenx)

#def yellowest(img, x_low, x_high, y_low, y_high):
##print(img.shape)
#    count = 0
#    x_low = int(x_low)
#    x_high = int(x_high)
#    y_low = int(y_low)
#    y_high = int(y_high)
#    yp = (0, 0)
#    old = 9999
#    for x in range(x_low, x_high, 5):
# #        print(x)
#         for y in range(y_low, y_high, 5):
#
#              print("{}".format((x, y)))
#              b, g, r = img[x,y]
#
#              if g>b and g>r:
#                 count = count + 1
## Old color: 80 200 0
#                 #olda = abs(img[yellowx,yellowy] - [100, 210, 220])
##                 olda = abs(img[greenx,greeny] - [80, 200, 0])
#                 #old = olda[0]+olda[1]+olda[2]
#                 newa = abs(img[x,y] - [70, 180, 180])
#                 new = newa[0]+newa[1]+newa[2]
#                 if new < old:
#                     old = new
#                     yp = (x, y)
##                     yellowx = x
##                     yellowy = y
#
##    print("Count is {}".format(count))
#    print("Yellow pixels at: {}".format(yp))
#    plt.imshow(img)
#    plt.show()
#    print("Yellow pixel values {}".format(img[yp[0], yp[1]]))
#    return (yp[1], yp[0])

def yellowest(img, x_low, x_high, y_low, y_high):
    global YELLOW
    x_low = int(x_low)
    x_high = int(x_high)
    y_low = int(y_low)
    y_high = int(y_high)
    yp = (0, 0)
    old= 9999
    for x in range(x_low, x_high, 10):
        for y in range(y_low, y_high, 10):
            b, g, r = img[x, y]
            #if y > b and y > r:
#            newa = abs(img[x, y] - [70, 180, 180])
            newa = abs(img[x, y] - YELLOW)   
            new = newa[0] + newa[1] + newa[2]
            if new < old:
                old = new
                yp = (x, y)
                #print ("green pixel values: {}".format(img[gp[0], gp[1]]))
    #print ("red pixel values: {}".format(img[rp[0], rp[1]]))
    #print("Yellow point location: {}".format(yp))
    #print("Yellow pixel values: {}".format(img[yp[0], yp[1]]))
    #plt.imshow(img)
    #plt.show()
    yp = (yp[1], yp[0])
    #print("Green point location: {}".format(gp))
    #print("Red point location: {}".format(rp))
    return yp

def redAndGreenDetection(img, x_low, x_high, y_low, y_high):
    global RED
    global GREEN
    x_low = int(x_low)
    x_high = int(x_high)
    y_low = int(y_low)
    y_high = int(y_high)
    gp = (0, 0)
    rp = (0, 0)
    old_g = 9999
    old_r = 9999
    for x in range(x_low, x_high, 10):
        for y in range(y_low, y_high, 10):
            b, g, r = img[x, y]
            if g > b and g > r:
#                newa = abs(img[x, y] - [120, 170, 85])
               newa = abs(img[x, y] - GREEN) 
               new = newa[0] + newa[1] + newa[2]
               if new < old_g:
                    old_g = new
                    gp = (x, y)
            elif r > b and r > g:
                newa = abs(img[x, y] - RED)
 #               newa = abs(img[x, y] - [170, 90, 90])
                new = newa[0] + newa[1] + 2*newa[2]
                if new < old_r:
                    old_r = new
                    rp = (x, y)
    #print ("green pixel values: {}".format(img[gp[0], gp[1]]))
    #print ("red pixel values: {}".format(img[rp[0], rp[1]]))
    rp = (rp[1], rp[0])
    gp = (gp[1], gp[0])
    #print("Green point location: {}".format(gp))
    #print("Red point location: {}".format(rp))
    return (rp, gp)

class Point(Structure):
   _fields_ = [("x", c_uint), ("y", c_uint)] 

class Pixel(Structure):
    _fields_ = [("b", c_ubyte), ("g", c_ubyte), ("r", c_ubyte)]


def findCorners(img):
    height, width, channels = img.shape
    #print (width, height)
    factor = 4


    c_module = cdll.LoadLibrary('./c/test.so')
    c_module.c_bluest.restype = Point

    c_blue_time = time.time()
#    print("Starting...")
    c_upper_left = c_module.c_bluest(img.ctypes.data_as(POINTER(c_ubyte)), 0, int(height/factor), 0, int(width/factor))
#    print("Found upper left")
    c_bottom_left = c_module.c_bluest(img.ctypes.data_as(POINTER(c_ubyte)), int(height - height/factor), height,  0, int(width/factor))
#    print("Found bottom left")
    c_upper_right = c_module.c_bluest(img.ctypes.data_as(POINTER(c_ubyte)), 0, int(height/factor),  int(width - width/factor), int(width)) 
#    print("Found upper_right")
    c_bottom_right = c_module.c_bluest(img.ctypes.data_as(POINTER(c_ubyte)), int(height- int(height/factor)), int(height),  int(width - int(width/factor)), int(width)) 
#    print("Found bottom right")
    
#    print("C: Upper left found at ({}, {})".format(c_upper_left.x, c_upper_left.y))
#    print("C: Upper right found at ({}, {})".format(c_upper_right.x, c_upper_right.y))
#    print("C: bottom left found at ({}, {})".format(c_bottom_left.x, c_bottom_left.y))
#    print("C: bottom right found at ({}, {})".format(c_bottom_right.x, c_bottom_right.y))
#    print("C: Corner detection took {}".format(time.time() - c_blue_time))

#    plt.imshow(img)
#    plt.show()


    #start = time.time()
    #upper_left =  bluest(img, 0,            height/factor,   0,         width/factor)
    ##print("Upper left found at {}".format(upper_left))
    #bottom_left = bluest(img, height - int(height/factor),     height,     0,         width/factor)
    #upper_right = bluest(img, 0,            height/factor,   width - int(width/factor),   width)
    #bottom_right = bluest(img, height - int(height/factor),    height,     width-(width/factor),   width)
    #end = time.time()
    #print("Corner detection took {} seconds".format(end - start))
    upper_left = (c_upper_left.x, c_upper_left.y)
    upper_right = (c_upper_right.x, c_upper_right.y)
    bottom_left = (c_bottom_left.x, c_bottom_left.y)
    bottom_right = (c_bottom_right.x, c_bottom_right.y)
    return (upper_left, bottom_left, upper_right, bottom_right)

def transform(img, corners=None):
    if corners == None:
        upper_left, bottom_left, upper_right, bottom_right = findCorners(img)
    else:
        upper_left, bottom_left, upper_right, bottom_right = corners
#    start = time.time()
#    height, width, channels = img.shape
#    #print (width, height)
#    factor = 5
#    upper_left =  bluest(img, 0,            height/factor,   0,         width/factor)
#    bottom_left = bluest(img, height - int(height/factor),     height,     0,         width/factor)
#    upper_right = bluest(img, 0,            height/factor,   width - int(width/factor),   width)
#    bottom_right = bluest(img, height - int(height/factor),    height,     width-(width/factor),   width)
#    end = time.time()
#    return (upper_left, bottom_left, upper_right, bottom_right)

    ##for x in range(0, img.shape[0], 10):
    ##     print(x)
    ##     for y in range(0, img.shape[1], 10):
    ##
    ##          b, g, r = img[x,y]
    ##
    ##          if b>g and b>r:
    ##             olda = abs(img[bluex,bluey] - [255,0,0])
    ##             old = olda[0]+olda[1]+olda[2]
    ##             newa = abs(img[x,y] - [255, 0, 0])
    ##             new = newa[0]+newa[1]+newa[2]
    ##             if new < old:
    ##                 bluex = x
    ##                 bluey = y

    #print(bluex, bluey)
    #print("Upper left: {} ({})".format(upper_left, img[upper_left[1],upper_left[0]]))
    #print("Upper right: {} ({})".format(upper_right, img[upper_right[1], upper_right[0]]))
    #print("Bottom left: {} ({})".format(bottom_left, img[bottom_left[1],bottom_left[0]]))
    #print("Bottom right: {} ({})".format(bottom_right, img[bottom_right[1], bottom_right[0]]))
#    print("Image for checking:")
#    plt.imshow(img)
#    plt.show()
    
    transformStart = time.time()
    height, width, channels = img.shape
    orig_pts = np.float32([upper_right, upper_left, bottom_left, bottom_right])
    new_pts = np.float32([(width, 0), (0, 0), (0, height), (width, height)])
    M = cv2.getPerspectiveTransform(orig_pts, new_pts)
    new_img = cv2.warpPerspective(img, M, (1600, 1200))
    transformEnd = time.time()
    #print("Transform duration: {}".format(transformEnd - transformStart))
    #cv2.imwrite('robot.jpg', new_img)
    #print("Transformed image")
    #plt.imshow(new_img)
    #plt.show()
    return new_img

if __name__ == '__main__':
    img = cv2.imread('im4.jpg')
    bluex = 0
    bluey = 0
    transform(img)
