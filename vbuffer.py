# Visual Buffer Team: Christopher Andrews
#                     Ian Hurd
#                     Angelo Tammaro

from typing import Type
import numpy as np

class VBuffer:
    
    def __init__(self, dimensions):
        # TODO
        # imageArray: a numpy array that holds the pixel data of a picture

        self._checkDoubleIntVal(dimensions, "dimensions", "__init__")
        xdim, ydim = dimensions[0], dimensions[1]
        if xdim <= 0 or ydim <= 0:
            raise ValueError("Buffer dimensions in vBuffer must exceed 0!")
        listGrid = [[0 for i in range(xdim)] for j in range(ydim)]
        self._buffer = np.array(listGrid)
        self._dimensions = (xdim, ydim)
        
        # debugFlag: a boolean variable
        self.debugFlag = False


    def _checkDoubleIntVal(self, val, argName, methodName):
        if type(val) is not list and type(val) is not tuple:
            raise TypeError(f"{argName} argument to vBuffer. {methodName} should be a list or a tuple!")
        elif len(val) != 2:
            raise TypeError(f"{argName} argument to vBuffer. {methodName} requires exactly 2 values!")
        elif type(val[0]) is not int or type(val[1]) is not int:
            raise TypeError(f"{argName} argument to vBuffer. {methodName} can only have integer values!")

        
    # Sets pixel at coordinates coords in buffer to hex value val
    def writePixel(self, coords, val):
        self._checkDoubleIntVal(coords, "coords", "writePixel")
        if type(val) is not int:
            raise TypeError("Color value must be an integer value!")
        elif val < 0 or val > 2**24:
            raise ValueError("Color value must remain an integer between 0 and 2^24!")
        x, y = coords[0], coords[1]
        self._buffer[x, y] = val

    def getPixel(self, coords):
        self._checkDoubleIntVal(coords, "coords", "getPixel")
        x, y = coords[0], coords[1]
        return self._buffer[x, y]
        
    # <insert definition of getDimensions function here>; X and Y are int variables
    def getDimensions(self):
        return self._dimensions

    # 
    def clearBuffer(self):
        self._buffer[:] = 0

    def getBuffer(self):
        return self._buffer
        
    
