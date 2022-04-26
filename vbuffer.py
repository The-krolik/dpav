import numpy as np


class VBuffer:
    """
    Visual buffer for the Python Direct Platform
    Constructor:
        __init__(self, dimensions)

    Setter:
        write_pixel(self, coords, val)
        set_buffer(self, buf)
        clear(self)

    Getters:
        get_pixel(self, coords)
        get_dimensions(self)
        get_buffer(self)

    Error Checking:
        _check_numpy_arr(self,arg1,arg_name,method_name)
        _check_coord_type(self, coords, arg_name, method_name)
        _check_coord_vals(self, x, y, method_name)
    """

    def __init__(self, arg1=(800, 600)):
        """
        Constructor for the VBuffer class.

        ERR CHECK:  if arg1 is not a numpy array; if the dimensions are
        greater than 1920x1080 or negative.

        Parameters
        ----------
        arg1 : {(int, int)|np.ndarray(int, int)}
            Either array dimensions or a 2-dimensional numpy array of integers

            If dimensions, will create zeroed-out 2D array of the selected
            dimensions. Defaults to 800x600.

            If numpy array, will set buffer to the contents of that array.
        """
        if type(arg1) is np.ndarray:
            dimensions = arg1.shape
            self._check_numpy_arr(arg1, "arg1", "__init__")
        else:
            self._check_coord_type(arg1, "arg1", "__init__")
            dimensions = arg1
            if dimensions[0] <= 0 or dimensions[1] <= 0:
                raise ValueError(f"dimensions must be greater than 0")
            elif dimensions[0] > 1920 or dimensions[1] > 1080:
                raise ValueError(
                    f"dimensions provided of size: {dimensions}, highest supported resolution is (1920,1080)"
                )

        self.buffer = (
            arg1 if type(arg1) is np.ndarray else np.zeros(dimensions, dtype=int)
        )
        self.debug_flag = False
        self._dimensions = dimensions

    def __getitem__(self, idx):
        """Return color value in buffer at selected coordinates.

        Parameters
        ----------
        idx : (int, int)
            Coordinates to retrieve color value from.
        """
        return self.buffer[idx]

    def __setitem__(self, idx, val):
        """Set color value at selected coordinates.

        Parameters
        ----------
        idx : (int, int)
            Coordinates to write to
        val : int
            Hex color code to write"""
        self.buffer[idx] = val

    def __len__(self):
        """Return the size of the buffer"""
        return len(self.buffer)

    @property
    def dimensions(self):
        """Return dimensions of buffer."""
        return self.buffer.shape

    @dimensions.setter
    def dimensions(self, val):
        """Return error; cannot reshape buffer by setting dimensions."""
        raise AttributeError("Cannot reshape visual buffer by setting dimensions")

    def _check_numpy_arr(self, arg1, arg_name, method_name):
        """Checks if value is a valid numpy array and raises exception if not

        Error checks for the following:
            - if arg1 is not a numpy array or a 2-element list/tuple
            - if arg1 doesn't fall within the range of 0-2^24
            - if arg1 isn't 2-dimensional
            - if arg1 tries to support resolutions higher than 1920x1080

        Parameters
        ----------
        arg1 : np.ndarray(int)
            Value to test.
        arg_name : string
            The name of the variable that is passed to this method as arg1.
            Will be used in error message for debugging purposes.
        method_name : string
            The name of the method in which this method is called.
            Will be used in error message for debugging purposes.
        """
        if not np.issubdtype(arg1.dtype, int) and not np.issubdtype(arg1.dtype, float):
            raise TypeError(
                f"{arg_name} argument to VBuffer. {method_name} must be of type numpy.ndarray dtype=int, or a 2 element dimension list/tuple!"
            )
        if np.any((arg1 < 0) | (arg1 > 16777215)):
            raise ValueError(
                f"{arg_name} argument to VBuffer. {method_name} must contain values in range 0 to 16777215"
            )
        if arg1.ndim != 2:
            raise TypeError(
                f"{arg_name} argument to VBuffer. {method_name} must be 2-dimensional numpy.ndarray"
            )
        if arg1.shape[0] > 1920 or arg1.shape[1] > 1080:
            raise ValueError(
                f"{arg_name} argument to VBuffer. {method_name} np.ndarray is of size: {arg1.shape} highest supported resolution is (1920,1080)"
            )

    def _check_coord_type(self, coords, arg_name, method_name) -> None:
        """Type checks coordinates, and raises exception if incorrect type.

        Error checks for the following:
            - if the coordinates are not stored in a list or a tuple
            - if the coordinates has more or less than two elements
            - if the values of the coordinates are not integer values

        Parameters
        ----------
        coords : (int, int)
            Value to test.
        arg_name : string
            The name of the variable that is passed to this method as coords.
            Will be used in error message for debugging purposes.
        method_name : string
            The name of the method in which this method is called.
            Will be used in error message for debugging purposes.
        """
        if type(coords) is not list and type(coords) is not tuple:
            raise TypeError(
                f"{arg_name} argument to VBuffer. {method_name} should be a list or a tuple!"
            )
        elif len(coords) != 2:
            raise TypeError(
                f"{arg_name} argument to VBuffer. {method_name} requires exactly 2 values!"
            )
        elif type(coords[0]) is not int or type(coords[1]) is not int:
            raise TypeError(
                f"{arg_name} argument to VBuffer. {method_name} can only have integer values!"
            )

    def _check_coord_val(self, coords, method_name) -> None:
        """Checks if supplied coordinates are valid. Raise exception if not.

        Error checks for the following:
            - if the X or Y coordinates are less than zero (0)
            - if the X or Y coordinates are out of bounds

        Parameters
        ----------
        coords : (int, int)
            Value to test.
        method_name : string
            The name of the method in which this method is called.
            Will be used in error message for debugging purposes.
        """
        x, y = coords[0], coords[1]
        if x < 0 or y < 0:
            raise ValueError(
                f"Coordinate args to VBuffer.{method_name} should be greater than zero."
            )
        elif x >= self.buffer.shape[0] or y >= self.buffer.shape[1]:
            raise ValueError(
                f"Coordinate args to VBuffer.{method_name} are out of bounds."
            )

    def write_pixel(self, coords, val) -> None:
        """Sets pixel at specified coordinates to specified color.

        Sets pixel at coordinates coords in buffer to hex value val
        ERR CHECK: if the color value is an integer; if the color value falls within the range of 0-2^24

        Parameters
        ----------
        coords : (int, int)
            Pixel coordinates (an X and a Y)
        val : int
            The hex value of the desired color to change the pixel with
        """
        self._check_coord_type(coords, "coods", "writePixel")
        self._check_coord_val(coords, "writePixel")
        if type(val) is not int:
            raise TypeError("Color value must be an integer value!")
        elif val < 0 or val > 0xFFFFFF:
            raise ValueError(f"Color value must be an integer between 0 and 16777215!")

        x, y = coords[0], coords[1]
        self.buffer[x, y] = val

    def get_pixel(self, coords) -> int:
        """Return color value of chosen pixel.

        Parameters
        ----------
        coords : (int, int)
            2-tuple or list containing first and second index of pixel
        """
        x, y = coords[0], coords[1]
        return self.buffer[x, y]

    def get_dimensions(self) -> "(int, int)":
        """Return dimensions of visual buffer array."""
        return self.buffer.shape

    def set_buffer(self, buf) -> None:
        """Set the visual buffer to equal a provided 2D array of pixels.

        Parameters
        ----------
        buf : np.ndarray(int, int)
            A 2-dimensional numpy array of integer color values
        """
        self._check_numpy_arr(buf, "buf", "set_buffer")
        self.buffer = buf

    def fill(self, color: int) -> None:
        """Set every pixel in the buffer to a given color.

        Parameters
        ----------
        color : int
            Hex color code
        """
        self.buffer[:] = color

    def clear(self) -> None:
        """Set every pixel in buffer to 0 (hex value for black)."""
        self.buffer[:] = 0

    def save_buffer_to_file(self, filename) -> None:
        """Save contents of buffer to a binary file.

        Parameters
        ----------
        filename : file path
            The path and name of the file to write to
        """
        np.save(filename, self.buffer)

    def load_buffer_from_file(self, filename) -> None:
        """Load binary file storing buffer contents, and write it to buffer.

        Parameters
        ----------
        filename : file path
            Path to a binary file containing numpy array data
        """
        self.buffer = np.load(filename + ".npy")
