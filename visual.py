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
        self.buffer = np.array(listGrid)
        self.dimensions = (xdim, ydim)
        
        # debugFlag: a boolean variable
        debugFlag = False
        
        
        
    # Sets pixel at coordinates coords in buffer to hex value val
    def writePixel(self, coords, val):
        x, y = coords[0], coords[1]
        self.buffer[x, y] = val
        
        
    # <insert definition of getDimensions function here>; X and Y are int variables
    def getDimensions(self):
        return self.dimensions
        
        
    # 
    def clearBuffer(self):
        self.buffer[:] = 0
        
    
