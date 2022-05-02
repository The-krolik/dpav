import numpy as np


class VBuffer:
    """
    Visual buffer for the Python Direct Platform

    Holds a 2D array of hex color values. Each element represents a pixel,
    whose coordinates are its index. VBuffer can be loaded and displayed by
    the window class.
    """

    def __init__(self, arg1: tuple = (800, 600)) -> None:
        """
        Constructor for the VBuffer class.

        Loads or creates 2D numpy array, which is the main body of the VBuffer.

        args:
            arg1: The desired dimensions of the visual buffer. Default value is
                (800, 600). May also be a numpy array, in which case it will load
                the contents of the array as well.

        Raises:
            TypeError: If arg1 is not of a valid type, or if its contents are not of
                a valid type.
            ValueError : If arg1 is of a valid type, but either of its values are
                negative, or greater than (1920, 1080).
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

    def __getitem__(self, idx: tuple) -> int:
        return self.buffer[idx]

    def __setitem__(self, idx: tuple, val: int) -> None:
        self.buffer[idx] = val

    def __len__(self) -> int:
        return len(self.buffer)

    @property
    def dimensions(self) -> tuple:
        """Returns the dimensions of the buffer."""
        return self.buffer.shape

    @dimensions.setter
    def dimensions(self, _) -> None:
        """
        Restricts user from manually changing dimensions.

        Raises:
            AttributeError: Always raises when setter is called.
        """
        raise AttributeError("Cannot reshape visual buffer by setting dimensions")

    def _check_numpy_arr(
        self, arg1: np.ndarray, arg_name: str, method_name: str
    ) -> None:
        """Checks if value is a valid numpy array and raises exception if not."""
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

    def _check_coord_type(self, coords: tuple, arg_name: str, method_name: str) -> None:
        """Type checks coordinates, and raises exception if incorrect type."""
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

    def _check_coord_val(self, coords: tuple, method_name: str) -> None:
        """Checks if supplied coordinates are valid. Raise exception if not."""
        x, y = coords[0], coords[1]
        if x < 0 or y < 0:
            raise ValueError(
                f"Coordinate args to VBuffer.{method_name} should be greater than zero."
            )
        elif x >= self.buffer.shape[0] or y >= self.buffer.shape[1]:
            raise ValueError(
                f"Coordinate args to VBuffer.{method_name} are out of bounds."
            )

    def write_pixel(self, coords: tuple, val: int) -> None:
        """
        Sets pixel at the specified coordinates to a specified color.

        Args:
            coords: Pixel coordinates (x, y).
            val: The hex value of the desired color.

        Raises:
            TypeError: If val is not an int.
            ValueError: If val is negative or greater than the max color
                value (0xFFFFFF).
        """
        self._check_coord_type(coords, "coords", "writePixel")
        self._check_coord_val(coords, "writePixel")
        if type(val) is not int:
            raise TypeError("Color value must be an integer value!")
        elif val < 0 or val > 0xFFFFFF:
            raise ValueError(f"Color value must be an integer between 0 and 16777215!")

        x, y = coords[0], coords[1]
        self.buffer[x, y] = val

    def get_pixel(self, coords: tuple) -> int:
        """Returns the color value of chosen pixel."""
        x, y = coords[0], coords[1]
        return self.buffer[x, y]

    def get_dimensions(self) -> tuple:
        """Returns the dimensions of the visual buffer"""
        return self.buffer.shape

    def set_buffer(self, buf: np.ndarray) -> None:
        """
        Set the contents of a visual buffer to match those of a given array.

        Args:
            buf: An array of hex color values.
        """
        self._check_numpy_arr(buf, "buf", "set_buffer")
        self.buffer = buf

    def fill(self, color: int) -> None:
        """Sets every pixel in the buffer to a given hex color value."""
        self.buffer[:] = color

    def clear(self) -> None:
        """Set every pixel in the buffer to 0 (hex value for black)."""
        self.fill(0)

    def save_buffer_to_file(self, filename: str) -> None:
        """
        Save contents of buffer to a binary file.

        Args:
            filename: The path and name of the file to write.
        """
        np.save(filename, self.buffer)

    def load_buffer_from_file(self, filename: str) -> None:
        """
        Load binary file storing buffer contents, and write it to buffer.

        Args:
            filename: The path to a binary file containing numpy array data.
        """
        self.buffer = np.load(filename + ".npy")
