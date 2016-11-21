import cv2
import numpy as np
import matplotlib.pyplot as plt
import PIL
import math
import time

def markBlock(img, pt, bs, height, width):
    #height, width, channels = img.shape
    
    if pt[1] + bs > height:
        ybound = height
    else:
        ybound = pt[1] + bs
    if pt[0] + bs > width:
        xbound = width
    else:
        xbound = pt[0] + bs
    #print('yb = ', ybound, 'xb = ', xbound)
    blockctr = 0
    freectr = 0
    for y in range(pt[1], ybound, 5):
            for x in range(pt[0], xbound, 5):
                if img[y,x] == 0:
                    #print("Found it!")
                    blockctr += 1
                else:
                    freectr +=1
    if blockctr > 0:
        return 0
    return 1


def mapToImage(m, sizex, sizey):
    img = np.zeros((sizey, sizex, 3), np.int8)
    for x in range(sizex):
        for y in range(sizey):
            if m[x][y] == 1:
                img[y, x] = [0, 0, 0]
            elif m[x][y] == 2:
                img[y, x] = [125, 125, 125]
            else:
                img[y, x] = [255, 255, 255]
    img = PIL.Image.fromarray(img, 'RGB')
    plt.imshow(img)
    plt.show()

def expandBoxes(rect, radius):
    rect =  (rect[0], (rect[1][0] + radius, rect[1][1] + radius), rect[2]) 
    return rect

#    if len(boxes) == 1:
#        boxes = [boxes]
#
#    for box in boxes:
#        center = ((box[0][0] + box[1][0] + box[2][0] + box[3][0]) / 4, (box[0][1] + box[1][1] + box[2][1] + box[3][1]) / 4)
#        print("Center found at {}".format(center))
#        for corner in box:
#            vector = corner - center
#            direction = vector / math.sqrt(vector[0] ** 2 + vector[1] ** 2)
#            newVector = vector + direction * radius
#            newVector = (int(newVector[0]), int(newVector[1]))
#            corner = center + newVector
            
    
def generateMap(img, radius):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Resize the image
#    smallGray = cv2.resize(img, None, fx = 0.05, fy = 0.05, interpolation = cv2.INTER_AREA)
#    print("Small gray image")
#    plt.imshow(smallGray)
#    plt.show()

#    plt.imshow(gray)
#    print("Grayscale image:")
#    plt.show() # Grayscale image
    #ret, thresh = cv2.threshold(gray, 85, 255, cv2.THRESH_BINARY_INV)
    #ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#    plt.imshow(thresh)
#    plt.show()
    _, conts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#    withoutExpansion = thresh.copy()
#    for c in conts:
#        rect = cv2.minAreaRect(c)
#        expandBoxes(rect, radius)
#        box = cv2.boxPoints(rect)
#        box= np.int0(box)
#        #rect = cv2.boundingRect(c)
#        #x,y,w,h = rect
#        #cv2.rectangle(thresh, (x,y), (x+w, y+h), 255, cv2.FILLED)
#        cv2.drawContours(withoutExpansion, [box], 0, (255,0,0), cv2.FILLED)
#    print("Image without expansion")
#    plt.imshow(withoutExpansion)
#    plt.show()
    
    new_radius = int(radius / 20)
    for c in conts:
        if cv2.contourArea(c) < math.pi * radius:
            continue
        rect = cv2.minAreaRect(c)
        rect = expandBoxes(rect, radius)
        box = cv2.boxPoints(rect)
        box= np.int0(box)
        #rect = cv2.boundingRect(c)
        #x,y,w,h = rect
        #cv2.rectangle(thresh, (x,y), (x+w, y+h), 255, cv2.FILLED)
        cv2.drawContours(thresh, [box], 0, (255,0,0), cv2.FILLED)

    M = cv2.resize(thresh, None, fx = 0.05, fy = 0.05, interpolation = cv2.INTER_AREA)
    height, width = M.shape
    m = [ [0 for y in range(height)] for x in range(width)]
    x = 0
    y = 0
    while (x < width and y < height):
        if x == 0 or y == 0 or x == width - 1 or y == height - 1 or M[y, x] > 0:
            m[x][y] = 1
        x = x + 1
        if x == width:
            x = 0
            y = y + 1
#    mapToImage(m, width, height)
        
    #_, m = cv2.threshold(m, 1, 255, cv2.THRESH_BINARY)

    #m = cv2.resize(thresh, (0, 0), 0.5, 0.5)
#    plt.imshow(m)
#    plt.show()

#    return m 

#    plt.imshow(thresh)
#    print("Bounded-box image")
#    plt.show()
##    plt.imshow(thresh)
##    print("Threshold-ed image:")
##    plt.show() # Thresholded image


#    bs = 20
#    height, width, channels = img.shape
#    #height = int(height / 2)
#    #width = int(width / 2)
#    blocks_x = math.ceil(width / bs)
#    blocks_y = math.ceil(height / bs)
#    m = [[0 for y in range(blocks_y)] for x in range(blocks_x)]
#    map_x = 0
#    map_y = 0
#    x = 0
#    y = 0
#    start = time.time()
#    while (x < width and y < height):
#        m[map_x][map_y] = markBlock(thresh, (x, y), bs, height, width)
#        if x == 0 or x == width-1:
#            m[map_x][map_y] = 1
#        if y == 0 or y == height-1:
#            m[map_x][map_y] = 1
#        map_x += 1
#        x += bs
#        if x >= width:
#            x = 0
#            y += bs
#            map_x = 0
#            map_y += 1
#    end = time.time()
#    print("Blocking marks duration: {}".format(end - start))


##    for i in range(height)+1:
##        m[i][0] = 1
##        m[i][height-1] = 1
##    for i in range(width)+1:
##        m[0][i] = 1
##        m[width-1][i] = 1
    #mapToImage(m, blocks_x, blocks_y)
    return m
    
 
