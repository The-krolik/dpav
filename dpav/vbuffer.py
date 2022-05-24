import numpy as np
from sdl2 import *
import sdl2.ext


class VBuffer:
    """
    Visual buffer for the Python Direct Platform

    Holds a 2D array of hex color values. Each element represents a pixel,
    whose coordinates are its index. VBuffer can be loaded and displayed by
    the window class.
    """

    def __init__(self, arg=(800, 600)) -> None:
        if type(arg) is str:
            # import from file
            raise Exception("Importing from a file is not yet implemented")
        elif type(arg) is np.ndarray:
            xdim, ydim = arg.shape
            arr = sdl2.ext.create_array(arg)
            self._surface = SDL_CreateRGBSurfaceWithFormatFrom(
                arr, xdim, ydim, 24, 3 * ydim, SDL_PIXELFORMAT_RGB888
            )
        else:
            xdim, ydim = arg
            self._surface = SDL_CreateRGBSurfaceWithFormat(
                0, xdim, ydim, 24, SDL_PIXELFORMAT_RGB888
            )

        self.buffer = sdl2.ext.pixels2d(self.surface, True)

    def __getitem__(self, idx: tuple) -> int:
        return self.buffer[idx]

    def __setitem__(self, idx: tuple, val: int) -> None:
        self.buffer[idx] = val

    def __len__(self) -> int:
        return len(self.buffer)

    @property
    def surface(self) -> SDL_Surface:
        return self._surface

    @surface.setter
    def surface(self, _) -> None:
        raise AttributeError("Cannot assign a surface to a visual buffer")

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

    def clear(self) -> None:
        """Set every pixel in the buffer to 0 (hex value for black)."""
        self.buffer.fill(0x000000)
