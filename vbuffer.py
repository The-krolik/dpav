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
            
        listGrid = [[0 for i in range(xdim)] for j in range(ydim)]
        self._buffer = np.array(listGrid)
        self._dimensions = (xdim, ydim)
        
        # debugFlag: a boolean variable
        self.debugFlag = False

        
    # Sets pixel at coordinates coords in buffer to hex value val
    #error check correct color value greater than 0 less than 2^32 
    #error check if unsigned int
    def writePixel(self, coords, val):
        x, y = coords[0], coords[1]
        self._buffer[x, y] = val

    def getPixel(self, coords):
        x, y = coords[0], coords[1]
        return self._buffer[x, y]
        
    # <insert definition of getDimensions function here>; X and Y are int variables
    def getDimensions(self):
        try:
            return self._dimensions
        except TypeError:
            raise TypeError("Error! x and y are meant to be integer values!")
        except ValueError:
            raise ValueError("Error! The values of x and y are meant to be integer values!")

    # 
    def clearBuffer(self):
        self._buffer[:] = 0

    def getBuffer(self):
        return self._buffer
        
    
