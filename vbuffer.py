# Visual Buffer Team: Christopher Andrews
#                     Ian Hurd
#                     Angelo Tammaro

import numpy as np

# TODO: color depth arg?

class VBuffer:
    """
    Visual buffer for the Python Direct Platform
    Constructor:
        __init__(self, dimensions)
    
    Setter:
        writePixel(self, coords, val)
        setBuffer(self, buf)
        clearBuffer(self)   
        
    Getters:
        getPixel(self, coords)
        getDimensions(self)
        getBuffer(self)     
    
    Error Checking:
        _checkNumpyArr(self,arg1,argName,methodName)
        _checkCoordType(self, coords, argName, methodName)
        _checkCoordVals(self, x, y, methodName)
    """
    
    def __init__(self, arg1 = (800, 600)):
        """
        Constructor for the VBuffer class.
        ERR CHECK:  if arg1 is not a numpy array; if the dimensions are greater than 1920x1080
        IN: a tuple/list of dimensions (800x600 default resolution)
        OUT: n/a
        """
        if type(arg1) is np.ndarray:
            dimensions = arg1.shape
            self._checkNumpyArr(arg1,"arg1","__init__")
        else:
            self._checkCoordType(arg1, "arg1", "__init__")
            dimensions = arg1
            if dimensions[0] <= 0 or dimensions[1] <= 0:
                raise ValueError(f"dimensions must be greater than 0")
            elif dimensions[0] > 1920 or dimensions[1] > 1080:
                raise ValueError(f"dimensions provided of size: {dimensions}, highest supported resolution is (1920,1080)")
        
        self.buffer = arg1 if type(arg1) is np.ndarray else np.zeros(dimensions, dtype=int)
        self.debugFlag = False
                
    def _checkNumpyArr(self,arg1,argName,methodName):
        """
        Error checks for the following:
            - if arg1 is not a numpy array or a 2-element list/tuple
            - if arg1 doesn't fall within the range of 0-2^24
            - if arg1 isn't 2-dimensional
            - if arg1 tries to support resolutions higher than 1920x1080
        """
        if not np.issubdtype(arg1.dtype, int) and not np.issubdtype(arg1.dtype,float):
            raise TypeError(f"{argName} argument to VBuffer. {methodName} must be of type numpy.ndarray dtype=int, or a 2 element dimension list/tuple!")
        if np.any((arg1 < 0)|(arg1 > 16777215)):
            raise ValueError(f"{argName} argument to VBuffer. {methodName} must contain values in range 0 to 16777215")
        if arg1.ndim != 2:
            raise TypeError(f"{argName} argument to VBuffer. {methodName} must be 2-dimensional numpy.ndarray")
        if arg1.shape[0] > 1920 or arg1.shape[1] > 1080:
            raise ValueError(f"{argName} argument to VBuffer. {methodName} np.ndarray is of size: {arg1.shape} highest supported resolution is (1920,1080)")
        
    def _checkCoordType(self, coords, argName, methodName):
        """
        Error checks for the following:
            - if the coordinates are not stored in a list or a tuple
            - if the coordinates has more or less than two elements
            - if the values of the coordinates are not integer values
        """
        if type(coords) is not list and type(coords) is not tuple:
            raise TypeError(f"{argName} argument to VBuffer. {methodName} should be a list or a tuple!")
        elif len(coords) != 2:
            raise TypeError(f"{argName} argument to VBuffer. {methodName} requires exactly 2 values!")
        elif type(coords[0]) is not int or type(coords[1]) is not int:
            raise TypeError(f"{argName} argument to VBuffer. {methodName} can only have integer values!")
        
    def _checkCoordVal(self, coords, methodName):
        """
        Error checks for the following:
            - if the X or Y coordinates are less than zero (0)
            - if the X or Y coordinates are out of bounds
        """
        x,y = coords[0],coords[1]
        if x < 0 or y < 0:
            raise ValueError(f"Coordinate args to VBuffer.{methodName} should be greater than zero.")
        elif x >= self.buffer.shape[0] or y >= self.buffer.shape[1]:
            raise ValueError(f"Coordinate args to VBuffer.{methodName} are out of bounds.")
        
    def writePixel(self, coords, val):
        """
        Sets pixel at coordinates coords in buffer to hex value val
        ERR CHECK: if the color value is an integer; if the color value falls within the range of 0-2^24
        IN: pixel coordinates (an X and a Y); the hex value of the desired color to change the pixel with
        OUT: n/a
        """
        self._checkCoordType(coords, "coods", "writePixel")
        self._checkCoordVal(coords, "writePixel")
        if type(val) is not int:
            raise TypeError("Color value must be an integer value!")
        elif val < 0 or val > 0xffffff:
            raise ValueError(f"Color value must be an integer between 0 and 16777215!")
            
        x, y = coords[0], coords[1]
        self.buffer[x, y] = val
      
    def getPixel(self, coords):
        x, y = coords[0], coords[1]
        return self.buffer[x, y]
        
    # <insert definition of getDimensions function here>; X and Y are int variables
    def getDimensions(self):
        return self.buffer.shape
    
    def setBuffer(self, buf):
        self._checkNumpyArr(buf, "buf", "setBuffer")
        self.buffer = buf      
        
    def clearBuffer(self):
        self.buffer[:] = 0
