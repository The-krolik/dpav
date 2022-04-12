# Visual Buffer Team: Christopher Andrews
#                     Ian Hurd
#                     Angelo Tammaro

from typing import Type
import numpy as np

# TODO: color depth arg?

class VBuffer:
    
    def __init__(self, arg1 = (600, 800)):
        if type(arg1) is np.ndarray:
            dimensions = arg1.shape
            self._checkNumpyArr(arg1,"arg1","__init__")
        else:
            self._checkCoordType(arg1, "arg1", "__init__")
            dimensions = arg1
            if dimensions[0] > 1920 or dimensions[1] > 1080:
                raise ValueError(f"dimensions provided of size: {dimensions}, highest supported resolution is (1920,1080)")
        
        self.buffer = arg1 if type(arg1) is np.ndarray else np.zeros(dimensions, dtype=int)
        self.debugFlag = False

                                
    def _checkNumpyArr(self,arg1,argName,methodName):
        if not np.issubdtype(arg1.dtype, int) and not np.issubdtype(arg1.dtype,float):
            raise TypeError(f"{argName} argument to VBuffer. {methodName} must be of type numpy.ndarray dtype=int, or a 2 element dimension list/tuple!")
        if np.any((arg1<0)|(arg1>16777215)):
            raise ValueError(f"{argName} argument to VBuffer. {methodName} must contain values in range 0 to 16777215")
        if arg1.ndim != 2:
            raise TypeError(f"{argName} argument to VBuffer. {methodName} must be 2-dimensional numpy.ndarray")
        if arg1.shape[0] > 1920 or arg1.shape[1] > 1080:
            raise ValueError(f"{argName} argument to VBuffer. {methodName} np.ndarray is of size: {arg1.shape} highest supported resolution is (1920,1080)")
        

    def _checkCoordType(self, coords, argName, methodName):
        if type(coords) is not list and type(coords) is not tuple:
            raise TypeError(f"{argName} argument to VBuffer. {methodName} should be a list or a tuple!")
        elif len(coords) != 2:
            raise TypeError(f"{argName} argument to VBuffer. {methodName} requires exactly 2 values!")
        elif type(coords[0]) is not int or type(coords[1]) is not int:
            raise TypeError(f"{argName} argument to VBuffer. {methodName} can only have integer values!")
        
    def _checkCoordVal(self, coords, methodName):
        x,y = coords[0],coords[1]
        if x < 0 or y < 0:
            raise ValueError(f"Coordinate args to VBuffer.{methodName} should be greater than zero.")
        elif x >= self.buffer.shape[0] or y >= self.buffer.shape[1]:
            raise ValueError(f"Coordinate args to VBuffer.{methodName} are out of bounds.")
        
    # Sets pixel at coordinates coords in buffer to hex value val
    #error check correct color value greater than 0 less than 2^24 
    #error check if int
    def writePixel(self, coords, val):
        self._checkCoordType(coords, "coords", "writePixel")
        self._checkCoordVal(coords, "coords", "writePixel")
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
        self._checkNumpyArr(buf,"buf", "setBuffer")
        self.buffer = buf
        
        
    # 
    def clearBuffer(self):
        self.buffer[:] = 0

    def getBuffer(self):
        return self.buffer
