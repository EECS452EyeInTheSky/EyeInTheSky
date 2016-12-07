from ctypes import *
import time
import numpy

class Point(Structure):
   _fields_ = [("x", c_uint), ("y", c_uint)]

pathfinding_module = cdll.LoadLibrary('./c/pathfinding.so')
pathfinding_module.find_path.restype = c_void_p
pathfinding_module.find_path.argtypes = [ POINTER(c_uint), Point, Point ]

pathfinding_module.find_path_length.restype = c_int
pathfinding_module.find_path_length.argtypes = [ c_void_p ]

pathfinding_module.get_path.restype = None

pathfinding_module.free_graph.restype = None
pathfinding_module.free_graph.argtypes = [c_void_p]

pathfinding_module.free_path.restype = None

def findPath_c(m, start_raw, goal_raw):
    m = numpy.array(m, dtype=numpy.uint32)
    start = Point(start_raw[0], start_raw[1])
    goal = Point(goal_raw[0], goal_raw[1])

    graph_p = pathfinding_module.find_path(m.ctypes.data_as(POINTER(c_uint)), start, goal)
    print("Found path!")
    path_len = pathfinding_module.find_path_length(graph_p)
    print("Found path length")
    if path_len == 0:
        print("Failed to find a path!")
        pathfinding_module.free_graph(graph_p)
        return None
    pathfinding_module.get_path.restype = POINTER(Point * path_len)
    raw_path_p = pathfinding_module.get_path(graph_p)
    raw_path = raw_path_p
    pathfinding_module.free_path.argtypes = [ POINTER(Point * path_len) ]
    path = []
    for p in raw_path.contents:
        path.append((p.x, p.y))
    #print (path)
    path.reverse()
    pathfinding_module.free_path(raw_path_p)
    pathfinding_module.free_graph(graph_p)
    
    return path
