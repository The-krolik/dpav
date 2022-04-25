import numpy as np
import pygame
import utility as util
from vbuffer import VBuffer
from typing import Union


class Window:
    """
    Handles Window capabilites of Python Direct Platform
    Functions:
        Constructor:
            __init__()

        Setters:
            set_scale(int/float)
            set_vbuffer(VBuffer/np.ndarray,optional:int)

        Getters:
            get_mouse_pos()

        Misc Methods:
            open()
            is_open()
            close()
            update()

        Private Methods:
            _update_events(pygame.event)
            _build_events_dict()
            _write_to_screen()

    Attributes:
        Public:
            vbuffer:     active VBuffer object
            scale:       number that scales up/down the size of the screen
                         (1.0 is unscaled)

            events:      dictionary of string:bool event pairs,
                         example:
                            "l_shift": True  -- left shift is pressed down
                            "l_shift": False -- left shift is not pressed

            eventq:      list of active events that occured since last update cycle
                         example:
                            ['l_shift', 'mouse', 'a', 'q']

            debug_flag:  boolean flag if window object should output debug info to log
            open_flag:   boolean flag for if the window is active

        Private:
            _keydict:    int:string PyGame event mapping. PyGame events identifiers are
                         stored as ints. This attribute is used by the public events
                         variable to map from PyGame's integer:boolean pairs to
                         our string:boolean pairs

            _surfaces    Two PyGame Surfaces for swapping to reflect vbuffer changes and
                         enable in-place nparray modification

            _screen      PyGame.display object, used for viewing vbuffer attribute
    """

    def __init__(
        self, arg1: Union[VBuffer, np.ndarray] = None, scale: Union[float, int] = 1.0
    ):
        """
        Constructor for the Window class.

        Args:
            arg1 (optional):
                VBuffer/np.ndarray (default None) to display on screen

                default:
                    if none provided, will create blank VBuffer with
                    dimensions: width = 800, height = 600

            scale (optional):
                float/int for scale of window
                default: 1.0
                example:
                    scale = 0.5, vbuffer dimensions = (800,600)
                    display dimensions = (400,300)

        Raises:
            TypeError:  arg1 VBuffer/np.ndarray type check
            TypeError:  scale int/float type check
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
        Returns the current mouse location with respect to the pygame window instance

        Raises:
            Runtime Error: no active pygame window instances exists
        """
        if self.open_flag == False:
            if self.debug_flag:
                util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")

        x = int(pygame.mouse.get_pos()[0] / self.scale)
        y = int(pygame.mouse.get_pos()[1] / self.scale)
        return (x, y)

    def set_vbuffer(self, arg1: Union[VBuffer, np.ndarray]) -> None:
        """
        Sets the vbuffer/nparray object to display on screen

        Args:
            arg1:  VBuffer/np.ndarray

        Raises:
            TypeError: arg1 VBuffer/np.ndarray type check
            TypeError: scale int/float type check
        """

        if arg1 == None or (type(arg1) is not np.ndarray and type(arg1) is not VBuffer):
            raise TypeError("Argument must be of type VBuffer or np.ndarray")

        self.vbuffer = arg1 if type(self.vbuffer) is VBuffer else VBuffer(arg1)

    def set_scale(self, scale: Union[float, int]) -> None:
        """
        Sets the window scale
        """

        self.scale = scale

    def open(self) -> None:
        """
        Creates and runs pygame window in a new thread
        """
        newx = self.vbuffer.get_dimensions()[0] * self.scale
        newy = self.vbuffer.get_dimensions()[1] * self.scale
        self._screen = pygame.display.set_mode((newx, newy))

        pygame.display.init()
        self.open_flag = True
        self._build_events_dict()

    def close(self) -> None:
        """
        Closes the active instance of a pygame window

        Raises:
            RuntimeError: no active pygame window instances exists
        """

        if not self.open_flag:
            if self.debug_flag:
                util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")

        self.open_flag, self._screen = False, None
        pygame.quit()

    def _write_to_screen(self) -> None:
        """
        Updates the screen with changes from stored vbuffer object
        """

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
        Updates events on every call, used to abstract out PyGame
        display calls and event loop

        example:
            if window.is_open():
               # your code here

        Return:
            boolean denoting if the window is currently open
        """

        self.update()
        return self.open_flag

    def update(self) -> None:
        """
        Pygame event abstraction, called at end of pygame loop.
        Optional function if is_open() is used

        Raises:
            Runtime Error: No active pygame window
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
        with pygame events

        Args:
            event: current event (string) to update
            example:
                self._update_events('l_shift')
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
        creates the events dictionary, called once by _start
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
