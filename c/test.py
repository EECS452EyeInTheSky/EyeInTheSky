from ctypes import *
import time

class Point(Structure):
   _fields_ = [("x", c_uint), ("y", c_uint)] 

class Pixel(Structure):
    _fields_ = [("b", c_ubyte), ("g", c_ubyte), ("r", c_ubyte)]

test_module = cdll.LoadLibrary("./test.so")

a = Pixel(100, 0, 0)
b = Pixel(0, 0, 255)

test_module.pixel_difference.restype = c_int

raw_result = test_module.pixel_difference(a, b)
result = raw_result
print (result)
