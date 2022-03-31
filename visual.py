# Visual Buffer Team: Christopher Andrews
#                     Ian Hurd
#                     Angelo Tammaro

import numpy as np

class Visual:
    
    def __init__(self, xdim, ydim):
        # TODO
        # imageArray: a numpy array that holds the pixel data of a picture
        listGrid = [[0 for i in range(xdim)] for j in range(ydim)]
        imageArray = np.array(listGrid)
        self.buffer = imageArray
        self.dimensions = (xdim, ydim)
        
        # debugFlag: a boolean variable
        debugFlag = False
        
        
        
    # Sets pixel at coordinates coords in buffer to hex value val
    def writePixel(coords, val):
        x, y = coords[0], coords[1]
        self.buffer[x, y] = val
        
        
    # <insert definition of getDimensions function here>; X and Y are int variables
    def getDimensions(self):
        return self.dimensions
        
        
    # 
    def clearBuffer():
        self.buffer[:,:] = 0
        
    
