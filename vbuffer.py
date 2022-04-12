# Visual Buffer Team: Christopher Andrews
#                     Ian Hurd
#                     Angelo Tammaro

from typing import Type
import numpy as np

class VBuffer:
    """
    Visual buffer for the Python Direct Platform
    Constructor:
        __init__(self, dimensions)
    
    Setter:
        writePixel(self, coords, val)
    
    Getters:
        getPixel(self, coords)
        getDimensions(self)
        getBuffer(self)
    
    Misc:
        _checkDoubleIntVal(self, val, argName, methodName)
        _checkCoordVals(self, x, y, methodName)
        clearBuffer(self)
    """
    
    def __init__(self, dimensions=(600, 800)):
        """
        Constructor for the VBuffer class.
        IN: dimensions for the image data
        OUT: n/a
        """
        self._checkDoubleIntVal(dimensions, "dimensions", "__init__")
        xdim, ydim = dimensions[0], dimensions[1]
        if xdim <= 0 or ydim <= 0:
            raise ValueError("Buffer dimensions in vBuffer must exceed 0!")

        #listGrid = [[0 for i in range(ydim)] for j in range(xdim)]
        #self._buffer = np.array(listGrid)
        self._buffer = np.zeros((xdim, ydim), dtype=int)
        self._dimensions = (xdim, ydim)
        self.debugFlag = False


    def _checkDoubleIntVal(self, val, argName, methodName):
        """
        Error checks for the following:
            - if val is not a list or a tuple
            - if val is not 2 elements
            - if the elements of val are not integers
        """
        if type(val) is not list and type(val) is not tuple:
            raise TypeError(f"{argName} argument to vBuffer. {methodName} should be a list or a tuple!")
        elif len(val) != 2:
            raise TypeError(f"{argName} argument to vBuffer. {methodName} requires exactly 2 values!")
        elif type(val[0]) is not int or type(val[1]) is not int:
            raise TypeError(f"{argName} argument to vBuffer. {methodName} can only have integer values!")

            
    def _checkCoordVals(self, x, y, methodName):
        """
        Error checks for the following:
            - if the X or Y coordinates are less than zero (0)
            - if the X or Y coordinates are out of bounds
        """
        if x < 0 or y < 0:
            raise ValueError(f"Coordinate args to VBuffer.{methodName} should be greater than zero.")
        elif x >= self._dimensions[0] or y >= self.dimensions[1]:
            raise ValueError(f"Coordinate args to VBuffer.{methodName} are out of bounds.")
        
     
    def writePixel(self, coords, val):
        """
        Sets pixel at coordinates coords in buffer to hex value val
        ERR CHECK: correct color value greater than 0 less than 2^24; if int
        IN: pixel coordinates (an X and a Y), the hex value of the desired color to change the pixel with
        OUT: n/a
        """
        self._checkDoubleIntVal(coords, "coords", "writePixel")
        if type(val) is not int:
            raise TypeError("Color value must be an integer value!")
        elif val < 0 or val > 2**24:
            raise ValueError("Color value must remain an integer between 0 and 2^24!")
        x, y = coords[0], coords[1]
        self._checkCoordVals(x, y, 'writePixel')
        self._buffer[x, y] = val

    
    def getPixel(self, coords):
        """
        Gets a pixel through the use of specified coordinates passed to the function as an array
        IN: array containing two coordinates (an X and a Y)
        OUT: returns the pixel at the specified coords
        """
        self._checkDoubleIntVal(coords, "coords", "getPixel")
        x, y = coords[0], coords[1]
        self._checkCoordVals(x, y, 'getPixel')
        return self._buffer[x, y]
        
    
    def getDimensions(self):
        """
        Gets the dimensions of the current image data
        IN: n/a
        OUT: returns the dimensions of the image data
        """
        return self._dimensions

    
    def clearBuffer(self):
        """
        Clears the visual buffer by setting all elements to zero
        IN: n/a
        OUT: n/a
        """
        self._buffer[:] = 0

        
    def getBuffer(self):
        """
        Gets the current visual buffer
        IN: n/a
        OUT: returns the visual buffer
        """
        return self._buffer
