# Visual Buffer Team: Christopher Andrews
#                     Ian Hurd
#                     Angelo Tammaro

import numpy as np

class VBuffer:
    
    def __init__(self, dimensions):
        # TODO
        # imageArray: a numpy array that holds the pixel data of a picture
        xdim, ydim = dimensions[0], dimensions[1]
        listGrid = [[0 for i in range(xdim)] for j in range(ydim)]
        self._buffer = np.array(listGrid)
        self._dimensions = (xdim, ydim)
        
        # debugFlag: a boolean variable
        self.debugFlag = False
        
        
    # Sets pixel at coordinates coords in buffer to hex value val
    def writePixel(self, coords, val):
        x, y = coords[0], coords[1]
        self._buffer[x, y] = val

    def getPixel(self, coords, isHex=False):
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
        
    
