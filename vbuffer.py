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
        clearBuffer(self)
    """
    
    def __init__(self, dimensions):
        """
        Constructor for the VBuffer class.
        IN: dimensions for the image data
        OUT: n/a
        """
        # error checking methods
        if type(dimensions) is not list and type(dimensions) is not tuple:
            raise TypeError("Error! Dimensions is supposed to be a list or tuple!")
        elif len(dimensions) != 2:
            raise ValueError("Error! Dimensions are only meant to be 2 values!")
        elif type(dimensions[0]) is not int or type(dimensions[1]) is not int:
            raise TypeError("Error! Dimensions are meant to be integer values! ")
        
        # set member data
        xdim, ydim = dimensions[0], dimensions[1]
        listGrid = [[0 for i in range(xdim)] for j in range(ydim)]
        self._buffer = np.array(listGrid)
        self._dimensions = (xdim, ydim)
        self.debugFlag = False
    
    
    def writePixel(self, coords, val):
        """
        Sets a pixel at the given coordinates in buffer to hex value val
        IN: pixel coordinates (an X and a Y), the hex value of the desired color to change the pixel with
        OUT: n/a
        """
        x, y = coords[0], coords[1]
        self._buffer[x, y] = val
        

    def getPixel(self, coords):
        """
        Gets a pixel through the use of specified coordinates passed to the function as an array
        IN: array containing two coordinates (an X and a Y)
        OUT: returns the pixel at the specified coords
        """
        x, y = coords[0], coords[1]
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
