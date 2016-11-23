import cv2
import numpy as np
import matplotlib.pyplot as plt 
import time
import math

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
    print("Searching in range x={} - {} and y={} - {}".format(x_low, x_high, y_low, y_high))
    x_low = int(x_low)
    x_high = int(x_high)
    y_low = int(y_low)
    y_high = int(y_high)
    bluex = 0
    bluey = 0
    old = 9999
    for x in range(x_low, x_high, 5):
         #print(x)
         for y in range(y_low, y_high, 5):

              b, g, r = img[x,y]

              if b>g and b>r:
                 #old = img[bluex,bluey][0]/(1+img[bluex,bluey][0]+img[bluex,bluey][1]+img[bluex,bluey][2])
                 # new = img[x,y][0]/(img[x,y][0]+img[x,y][1]+img[x,y][2]+1)
                 #olda = abs(img[bluex,bluey] - [255,0,0])
                 #old = 2*olda[0]+olda[1]+olda[2]
                 newa = abs(img[x,y] - [255, 0, 0])
                 new = 2*newa[0]+newa[1]+newa[2]
                 if new < old:
                     old = new
                     bluex = x
                     bluey = y
                     
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

def redAndGreenDetection(img, x_low, x_high, y_low, y_high):
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
                newa = abs(img[x, y] - [80, 200, 0])
                new = newa[0] + newa[1] + newa[2]
                if new < old_g:
                    old_g = new
                    gp = (x, y)
            elif r > b and r > g:
                newa = abs(img[x, y] - [0, 0, 255])
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

def findCorners(img):
    start = time.time()
    height, width, channels = img.shape
    #print (width, height)
    factor = 4
    upper_left =  bluest(img, 0,            height/factor,   0,         width/factor)
    bottom_left = bluest(img, height - int(height/factor),     height,     0,         width/factor)
    upper_right = bluest(img, 0,            height/factor,   width - int(width/factor),   width)
    bottom_right = bluest(img, height - int(height/factor),    height,     width-(width/factor),   width)
    end = time.time()
    print("Corner detection took {} seconds".format(end - start))
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
