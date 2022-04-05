# Visual Buffer Team: Christopher Andrews
#                     Ian Hurd
#                     Angelo Tammaro

<<<<<<< HEAD
from typing import Type
=======
>>>>>>> 266851bdff7c6f4dc1c276314282daf9434dfa6f
import numpy as np

class VBuffer:
    
    def __init__(self, dimensions):
        # TODO
        # imageArray: a numpy array that holds the pixel data of a picture
        if type(dimensions) is not list and type(dimensions) is not tuple:
            raise TypeError("Error! Dimensions is supposed to be a list or tuple!")
        elif len(dimensions) != 2:
            raise ValueError("Error! Dimensions are only meant to be 2 values!")
<<<<<<< HEAD
        elif type(dimensions[0]) is not int and type(dimensions[1]) is not int:
=======
        elif type(dimensions[0]) is not int or type(dimensions[1]) is not int:
>>>>>>> 266851bdff7c6f4dc1c276314282daf9434dfa6f
            raise TypeError("Error! Dimensions are meant to be integer values! ")


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

    def getPixel(self, coords):
        x, y = coords[0], coords[1]
        return self._buffer[x, y]
        
    # <insert definition of getDimensions function here>; X and Y are int variables
    def getDimensions(self):
<<<<<<< HEAD
        try:
            return self._dimensions
        except TypeError:
            raise TypeError("Error! x and y are meant to be integer values!")
        except ValueError:
            raise ValueError("Error! The values of x and y are meant to be integer values!")

=======
        return self._dimensions
        
        
>>>>>>> 266851bdff7c6f4dc1c276314282daf9434dfa6f
    # 
    def clearBuffer(self):
        self._buffer[:] = 0

    def getBuffer(self):
        return self._buffer
        
    
