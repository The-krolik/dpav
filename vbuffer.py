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
        write_pixel(self, coords, val)
        set_buffer(self, buf)
        clear_buffer(self)   
        
    Getters:
        get_pixel(self, coords)
        get_dimensions(self)
        get_buffer(self)     
    
    Error Checking:
        _check_numpy_arr(self,arg1,arg_name,method_name)
        _check_coord_type(self, coords, arg_name, method_name)
        _check_coord_vals(self, x, y, method_name)
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
            self._check_numpy_arr(arg1,"arg1","__init__")
        else:
            self._check_coord_type(arg1, "arg1", "__init__")
            dimensions = arg1
            if dimensions[0] <= 0 or dimensions[1] <= 0:
                raise ValueError(f"dimensions must be greater than 0")
            elif dimensions[0] > 1920 or dimensions[1] > 1080:
                raise ValueError(f"dimensions provided of size: {dimensions}, highest supported resolution is (1920,1080)")
        
        self.buffer = arg1 if type(arg1) is np.ndarray else np.zeros(dimensions, dtype=int)
        self.debug_flag = False
                
    def _check_numpy_arr(self,arg1,a rg_name, method_name):
        """
        Error checks for the following:
            - if arg1 is not a numpy array or a 2-element list/tuple
            - if arg1 doesn't fall within the range of 0-2^24
            - if arg1 isn't 2-dimensional
            - if arg1 tries to support resolutions higher than 1920x1080
        """
        if not np.issubdtype(arg1.dtype, int) and not np.issubdtype(arg1.dtype,float):
            raise TypeError(f"{arg_name} argument to VBuffer. {method_name} must be of type numpy.ndarray dtype=int, or a 2 element dimension list/tuple!")
        if np.any((arg1 < 0)|(arg1 > 16777215)):
            raise ValueError(f"{arg_name} argument to VBuffer. {method_name} must contain values in range 0 to 16777215")
        if arg1.ndim != 2:
            raise TypeError(f"{arg_name} argument to VBuffer. {method_name} must be 2-dimensional numpy.ndarray")
        if arg1.shape[0] > 1920 or arg1.shape[1] > 1080:
            raise ValueError(f"{arg_name} argument to VBuffer. {method_name} np.ndarray is of size: {arg1.shape} highest supported resolution is (1920,1080)")
        
    def _check_coord_type(self, coords, arg_name, method_name):
        """
        Error checks for the following:
            - if the coordinates are not stored in a list or a tuple
            - if the coordinates has more or less than two elements
            - if the values of the coordinates are not integer values
        """
        if type(coords) is not list and type(coords) is not tuple:
            raise TypeError(f"{arg_name} argument to VBuffer. {method_name} should be a list or a tuple!")
        elif len(coords) != 2:
            raise TypeError(f"{arg_name} argument to VBuffer. {method_name} requires exactly 2 values!")
        elif type(coords[0]) is not int or type(coords[1]) is not int:
            raise TypeError(f"{arg_name} argument to VBuffer. {method_name} can only have integer values!")
        
    def _check_coord_val(self, coords, method_name):
        """
        Error checks for the following:
            - if the X or Y coordinates are less than zero (0)
            - if the X or Y coordinates are out of bounds
        """
        x,y = coords[0],coords[1]
        if x < 0 or y < 0:
            raise ValueError(f"Coordinate args to VBuffer.{method_name} should be greater than zero.")
        elif x >= self.buffer.shape[0] or y >= self.buffer.shape[1]:
            raise ValueError(f"Coordinate args to VBuffer.{method_name} are out of bounds.")
        
    def write_pixel(self, coords, val):
        """
        Sets pixel at coordinates coords in buffer to hex value val
        ERR CHECK: if the color value is an integer; if the color value falls within the range of 0-2^24
        IN: pixel coordinates (an X and a Y); the hex value of the desired color to change the pixel with
        OUT: n/a
        """
        self._check_coord_type(coords, "coods", "writePixel")
        self._check_coord_val(coords, "writePixel")
        if type(val) is not int:
            raise TypeError("Color value must be an integer value!")
        elif val < 0 or val > 0xffffff:
            raise ValueError(f"Color value must be an integer between 0 and 16777215!")
            
        x, y = coords[0], coords[1]
        self.buffer[x, y] = val
      
    def get_pixel(self, coords):
        x, y = coords[0], coords[1]
        return self.buffer[x, y]
        
    # <insert definition of getDimensions function here>; X and Y are int variables
    def get_dimensions(self):
        return self.buffer.shape
    
    def set_buffer(self, buf):
        self._check_numpy_arr(buf, "buf", "setBuffer")
        self.buffer = buf      
        
    def clear_buffer(self):
        self.buffer[:] = 0
