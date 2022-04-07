# Visual Buffer Team: Christopher Andrews
#                     Ian Hurd
#                     Angelo Tammaro

import numpy as np

class VBuffer:
    
    # Constructor; Called each time a VBuffer object is created; Initializes member data;
    def __init__(self, dimensions):
        # error checking
        if type(dimensions) is not list and type(dimensions) is not tuple:
            raise TypeError("Error! Dimensions is supposed to be a list or tuple!")
        elif len(dimensions) != 2:
            raise ValueError("Error! Dimensions are only meant to be 2 values!")
        elif type(dimensions[0]) is not int or type(dimensions[1]) is not int:
            raise TypeError("Error! Dimensions are meant to be integer values! ")

        xdim, ydim = dimensions[0], dimensions[1]
        listGrid = [[0 for i in range(xdim)] for j in range(ydim)]
        self._buffer = np.array(listGrid)
        self._dimensions = (xdim, ydim)
        
        self.debugFlag = False

        
    # Sets pixel at coordinates coords in buffer to hex value val
    def writePixel(self, coords, val):
        x, y = coords[0], coords[1]
        self._buffer[x, y] = val

    # Function used to get a specific pixel through the use of specified coordinates passed to the function as an array
    def getPixel(self, coords):
        x, y = coords[0], coords[1]
        return self._buffer[x, y]
        
    # Function used to get the dimensions of the current image data
    def getDimensions(self):
        return self._dimensions
        
        
    # Function used to clear the visual buffer; Sets all elements to zero
    def clearBuffer(self):
        self._buffer[:] = 0

    # Function used to get the current visual buffer
    def getBuffer(self):
        return self._buffer
