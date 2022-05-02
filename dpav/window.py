from dpav import VBuffer, utility as util
import numpy as np
import pygame


class Window:
    """
    Handles Window capabilites of Direct Python Audio/Video.

    Attributes:
        vbuffer (:obj:`VBuffer`): The currently active visual buffer.
        scale (float): A number that scales up/down the size of the screen (1.0 is unscaled).
        events: A dictionary of string:bool event pairs.
        eventq (list): The active events that occured since last update cycle.
        debug_flag (bool): A flag for whether or not the window object should output debug info to log
        open_flag (bool): A flag for whether or not the window is active.
        _keydict: int:string PyGame event mapping. PyGame events identifiers are
            stored as ints. This attribute is used by the public events
            variable to map from PyGame's integer:boolean pairs to
            our string:boolean pairs.
        _surfaces (list): Two PyGame Surfaces for swapping to reflect vbuffer changes and
            to enable in-place nparray modification.
        _screen: A PyGame.display object, used for viewing vbuffer attribute.
    """

    def __init__(self, arg1: VBuffer = None, scale: float = 1.0):
        """
        The constructor for the Window class.

        Args:
            arg1 (optional): VBuffer/np.ndarray (default None) to display on screen.

                default: Will create blank VBuffer with dimensions: width = 800, height = 600.

            scale (optional): A float for the scale of window (default is 1.0).

        Raises:
            TypeError: If arg1 is not either a VBuffer or np.ndarray.
            TypeError: If the scale is not a float.
        """

        if arg1 != None and (
            type(arg1) is not VBuffer and type(arg1) is not np.ndarray
        ):
            raise TypeError("arg1 must be of type VBuffer or np.ndarray")
        if type(scale) is not int and type(scale) is not float:
            raise TypeError("arg2 must be of type Int")

        if arg1 == None:
            arg1 = VBuffer((800, 600))
        elif type(arg1) == np.ndarray:
            arg1 = VBuffer(arg1)

        ### Public Members ###
        self.vbuffer = arg1
        self.scale = scale
        self.events = {}
        self.eventq = []
        self.debug_flag = False
        self.open_flag = False

        ### Private Members ###
        self._surfaces = {
            "active": pygame.Surface(self.vbuffer.get_dimensions()),
            "inactive": pygame.Surface(self.vbuffer.get_dimensions()),
        }
        self._keydict = {}
        self._screen = None

    def get_mouse_pos(self) -> (int, int):
        """
        Returns the current mouse location.

        Returns:
            A tuple containing the coordinates of the current mouse location in the window.

        Raises:
            Runtime Error: If no active pygame window instances exists.
        """
        if self.open_flag == False:
            if self.debug_flag:
                util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")

        x = int(pygame.mouse.get_pos()[0] / self.scale)
        y = int(pygame.mouse.get_pos()[1] / self.scale)
        return (x, y)

    def set_vbuffer(self, arg1: VBuffer) -> None:
        """
        Sets the visual buffer object to display on screen.

        Args:
            arg1: The visual buffer to display.

        Raises:
            TypeError: If arg1 is not either a VBuffer or a np.ndarray.
            TypeError: If the scale is not a float.
        """

        if arg1 == None or (type(arg1) is not np.ndarray and type(arg1) is not VBuffer):
            raise TypeError("Argument must be of type VBuffer or np.ndarray")

        self.vbuffer = arg1 if type(self.vbuffer) is VBuffer else VBuffer(arg1)

    def set_scale(self, scale: float) -> None:
        """Sets the window scale."""

        self.scale = scale

    def open(self) -> None:
        """Creates and runs pygame window."""
        newx = self.vbuffer.get_dimensions()[0] * self.scale
        newy = self.vbuffer.get_dimensions()[1] * self.scale
        self._screen = pygame.display.set_mode((newx, newy))

        pygame.display.init()
        self.open_flag = True
        self._build_events_dict()

    def close(self) -> None:
        """
        Closes the active instance of a pygame window.

        Raises:
            RuntimeError: If no active pygame window exists.
        """

        if not self.open_flag:
            if self.debug_flag:
                util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")

        self.open_flag, self._screen = False, None
        pygame.quit()

    def _write_to_screen(self) -> None:
        """Updates the screen with changes from stored vbuffer object."""

        # swap surfaces
        self._surfaces["active"], self._surfaces["inactive"] = (
            self._surfaces["inactive"],
            self._surfaces["active"],
        )

        pygame.surfarray.blit_array(self._surfaces["active"], self.vbuffer.buffer)

        if self._screen != None and self.open_flag:
            x = self.vbuffer.get_dimensions()[0] * self.scale
            y = self.vbuffer.get_dimensions()[1] * self.scale
            scaled = pygame.transform.scale(self._surfaces["active"], (x, y))

            self._screen.blit(scaled, (0, 0))
            pygame.display.flip()

    def is_open(self) -> bool:
        """
        Method that the user can check in a while loop to maintain a window.

        This call updates events on every call and is used to abstract out PyGame
        display calls as well as the event loop.

        example:
            if window.is_open():
               # your code here

        Returns:
            A boolean value denoting whether or not the window is currently open.
        """

        self.update()
        return self.open_flag

    def update(self) -> None:
        """
        Updates the Pygame window to display changes made to the visual buffer.

        Note:
            This function's use is optional if is_open() is used.

        Raises:
            Runtime Error: If there is no active pygame window.
        """
        self._write_to_screen()
        if self.open_flag == False:
            if self.debug_flag:
                util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")
        else:
            self.eventq.clear()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()

                self._update_events(event)

    def _update_events(self, event: str) -> None:
        """
        Updates the Window class event dictionary to maintain continuity
        with pygame events.

        Args:
            event: The current event (string) to update.
        """

        strkey = "None"

        # if mouse, intkey = event.type, else set to pygame key value
        intkey = event.dict.get("key") if event.type in [768, 769] else event.type

        if intkey == None:
            strkey = "None"
        elif intkey in self._keydict:
            strkey = self._keydict[intkey]

        if strkey != "None" and strkey in self.events:
            self.events[strkey] = True if self.events[strkey] == False else False

            if self.events[strkey]:
                self.eventq.append(strkey)
            if self.debug_flag:
                util._debugOut("key '{}' set to {}".format(strkey, self.events[strkey]))

    def _build_events_dict(self) -> None:
        """
        Creates the events dictionary. This function is called once by _start.
        """

        # used for mapping of pygame key int identifiers to string identifiers
        self._keydict = {
            pygame.K_F1: "f1",
            pygame.K_F2: "f2",
            pygame.K_F3: "f3",
            pygame.K_F4: "f4",
            pygame.K_F5: "f5",
            pygame.K_F6: "f6",
            pygame.K_F7: "f7",
            pygame.K_F8: "f8",
            pygame.K_F9: "f9",
            pygame.K_F10: "f10",
            pygame.K_F11: "f11",
            pygame.K_F12: "f12",
            pygame.MOUSEBUTTONDOWN: "mouse",
            pygame.MOUSEBUTTONUP: "mouse",
            pygame.K_SPACE: "space",
            1073742049: "l_shift",
            1073742053: "r_shift",
            1073742048: "l_ctrl",
            1073742052: "r_ctrl",
            1073742050: "l_alt",
            1073742054: "r_alt",
            1073741881: "caps_lock",
            1073741904: "l_arrow",
            1073741903: "r_arrow",
            1073741905: "d_arrow",
            1073741906: "u_arrow",
        }

        # add [a-z] to dict
        for code in range(ord("a"), ord("z") + 1):
            self._keydict[code] = chr(code)

        # add [, - . /] and [0-9] to dict
        for code in range(ord(","), ord("9") + 1):
            self._keydict[code] = chr(code)

        # create events dict from _keydict string mappings
        for key, value in self._keydict.items():
            self.events[value] = pygame.key.get_pressed()[key]
