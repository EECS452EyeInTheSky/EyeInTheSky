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
import time

def findPath(m, start, finish, radius):
    graph = Graph(m, start, finish)
    path = graph.findPath()
    return path
    
class Node:
    def __init__(self, m, pos, finish, start):
        self.neighbors = []
        self.pos = pos
        self.prev = None
        self.visited = False
#        print("Pos is {}".format(pos))

        if pos[0] == finish[0] and pos[1] == finish[1]:
            self.cost = 0
#        elif m[pos[0]][pos[1]] == 1:
#            self.cost = float('inf')
#            self.cost = 99999999999999
#            self.visited = True
        else:
            self.cost = float('inf')

        self.heur = math.sqrt((pos[0]-start[0])**2 + (pos[1]-start[1])**2)
            
    def findMinNeighbor(self):
        minNeigh = None
        for neigh in self.neighbors:
            if minNeigh == None or minNeigh.cost > neigh.cost:
                minNeigh = neigh

    def score(self):
        return self.cost + self.heur 
    
    # Approximates dist, but only for pixels next to each other
#    def distScore(self, other):
#        if self.pos[0] != other.pos[0] and self.pos[1] != other.pos[1]:
#            return 1.414
#        else:
#            return 1

    def dist(self, other):
        return math.sqrt((self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2)


    def assignNeighbors(self, g):
        if self.pos[0] > 0 and self.pos[1] > 0:
            node = g.findNode((self.pos[0]-1, self.pos[1]-1))
            if node != None:
                self.neighbors.append(node)
        if self.pos[0] > 0:
            node = g.findNode((self.pos[0]-1, self.pos[1]))
            if node != None:
                self.neighbors.append(node)
#            self.neighbors.append(g.findNode((self.pos[0]-1, self.pos[1])))
        if self.pos[0] > 0 and self.pos[1] < g.My-1:
            node = g.findNode((self.pos[0]-1, self.pos[1]+1))
            if node != None:
                self.neighbors.append(node)
#            self.neighbors.append(g.findNode((self.pos[0]-1, self.pos[1]+1)))
        if self.pos[1] > 0:
            node = g.findNode((self.pos[0], self.pos[1]-1))
            if node != None:
                self.neighbors.append(node)
#            self.neighbors.append(g.findNode((self.pos[0], self.pos[1]-1)))
        if self.pos[1] < g.My - 1:
            node = g.findNode((self.pos[0], self.pos[1]+1))
            if node != None:
                self.neighbors.append(node)
#            self.neighbors.append(g.findNode((self.pos[0], self.pos[1]+1)))
        if self.pos[0] < g.Mx - 1 and self.pos[1] > 0:
            node = g.findNode((self.pos[0]-1, self.pos[1]-1))
            if node != None:
                self.neighbors.append(node)
#            self.neighbors.append(g.findNode((self.pos[0]+1, self.pos[1]-1)))
        if self.pos[0] < g.Mx - 1:
            node = g.findNode((self.pos[0]+1, self.pos[1]))
            if node != None:
                self.neighbors.append(node)
#            self.neighbors.append(g.findNode((self.pos[0]+1, self.pos[1])))
        if self.pos[0] < g.Mx - 1 and self.pos[1] < g.My - 1:
            node = g.findNode((self.pos[0]+1, self.pos[1]+1))
            if node != None:
                self.neighbors.append(node)
#            self.neighbors.append(g.findNode((self.pos[0]+1, self.pos[1]+1)))

        # Remove neighbors with infinite cost (They are obstacles and can't be traversed)
#        for n in self.neighbors:
#            if n.cost != None and math.isinf(n.cost):
##                print("Removed a neighbor")
#                self.neighbors.remove(n)
        

class Graph:
    def __init__(self, m, pos, finish):
        self.Mx = len(m)
        self.My = len(m[0])
        self.nodes = []
        self.nodeDict = dict()
        self.start = pos
        self.finish = finish
        self.searchNodes = []

        print("Generating nodes...")
        for x in range(self.Mx):
            for y in range(self.My):
                if m[x][y] == 1:
                    self.nodeDict[(x, y)] = None
                else:
                    node = Node(m, (x, y), finish, self.start)
                    self.nodes.append(node)
                    self.nodeDict[(x, y)] = node
        self.searchNodes.append(self.findNode((self.finish)))
        print("Finished generating nodes")

        #for node in self.nodes:
        #    if node.cost > 0:
    

        print("Assigning neighbors...")
        for node in self.nodes:
            node.assignNeighbors(self)
        print("Finished assigning neighbors")
#        for node in self.nodes:
#            if node.cost != None and math.isinf(node.cost) or m[node.pos[0]][node.pos[1]] == 1:
#                self.nodes.remove(node)

    def findNode(self, targetPos):
        return self.nodeDict[targetPos]
            
    def findPath(self):
        startTime = time.time()
        first = True
#        while len(self.nodes) > 0:
        while len(self.searchNodes) > 0:
#            next = self.findNode(self.finish)
#            print("Nodes left to process: {}".format(len(self.nodes)))
#            if first:
#                next = self.findNode(self.finish)
#                first = False
#            else:
#                next = self.findMinNode()
#            print("Next node position and score: {}, {}".format(next.pos, next.cost, next.score))
#            print("Next node neighbors: {}".format(next.neighbors))
#            self.nodes.remove(next)
            cur = self.findMinNode()
            self.searchNodes.remove(cur)
            cur.visited = True

            for neigh in cur.neighbors:
#                if neigh.visited or (neigh.cost != None and math.isinf(neigh.cost)): 
                if neigh.visited:
                    continue
                if cur.cost + cur.dist(neigh) < neigh.cost:
#                if cur.cost + cur.distScore(neigh) < neigh.cost:
                    neigh.cost = cur.cost + cur.dist(neigh)
#                    neigh.cost = cur.cost + cur.distScore(neigh)
                    neigh.prev = cur
                    self.searchNodes.append(neigh)
#            print("Next node neighbor cost after updating:")
#            for n in cur.neighbors:
#                print("{} has cost of {}, heur of {}".format(n.pos, n.cost, n.heur))
#            sleep(10)
            if cur.pos == self.start:
                break

        path = []
        cur = self.nodeDict[self.start]
#        print("Cur is at {}".format(cur.pos))
#        while cur.pos[0] != self.finish[0] and cur.pos[1] != self.finish[1]:
        while cur.prev != None:
            path.append(cur.pos)
   #         print("We can reach {} via {}".format(cur.pos, cur.prev.pos))
            cur = cur.prev    
        end = time.time()
        print("Duration for path finding: {}".format(end - startTime))
        return path
    
    def findMinNode(self):
        minNode = None
#        for node in self.nodes:
        for node in self.searchNodes:
#            if math.isinf(node.cost):
#                continue
#            print("Didn't skip a node")
            if minNode == None or minNode.score() > node.score():
#                print("minNode changed to node at {} with score {}".format(node.pos, node.score()))
                minNode = node
        return minNode

#        minNode = None
#        for node in self.nodes:
#            if node.cost == None or math.isinf(node.cost):
#                continue
#            if minNode == None or minNode.cost == None or minNode.cost > node.cost:
#                minNode = node
#        return minNode    
        
    
