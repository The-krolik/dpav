import numpy as np
import pygame
import utility as util
from vbuffer import VBuffer
import threading


class Action:
    """
    Data Structure to hold key/function pairs

    Members:
        key      -- string   -- key to trigger function
        function -- function -- function to trigger
    """

    def __init__(self, key, function):
        self.key = key
        self.function = function


class Window:
    """
    Handles Window capabilites of Python Direct Platform
    Functions:
        Constructor:
            __init__()

        Setters:
            set_vbuffer(VBuffer/np.ndarray,optional:int)

        Getters:
            get_mouse_pos()

        Misc Methods:
            open()
            close()
            update()

            new_action(function,optional:tuple/list)
            new_press_action(str,function,optional:tuple/list)
            new_hold_action(str,funcion,optional:tuple/list)

            write_to_screen()

        Private Methods:

            _start()
            _check_valid_action(str,function,string)
            _update_events(pygame.event)
            _build_events_dict()

    Members:
        Public:
            vbuffer        -- VBuffer          -- active VBuffer object
            scale          -- int/float        -- scales up/down size of screen
            events         -- {string:bool}    -- dictionary of string:bool event pairs
            eventq         -- [event]          -- queue of events since last update cycle
            debugflag      -- Boolean          -- debug logging on/off
            is_open        -- Boolean          -- flag for if the window is active

        Private:
            _keydict       -- {int:string}     -- Mapping of pygame int event idenitifiers to strings
            _actions       -- [Action]         -- Actions always triggered in event loop
            _press_actions -- [Action]         -- Actions triggered on key press in event loop
            _hold_actions  -- [Action]         -- Actions triggered on key hold in event loop
            _surfaces      -- {pygame.Surface} -- Two surfaces for swapping to reflect vbuffer changes
            _screen        -- pygame.display   -- pygame window


    """

    def __init__(self, arg1=None, scale=1):
        """
        Constructor for the Window class.

        Positional arguments:
            arg1  -- VBuffer/np.ndarray (default None)
            scale -- float/int (default 1)

        Raises:
            TypeError -- arg1 VBuffer/np.ndarray type check
            TypeError -- scale int/float type check
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
        self.is_open = False
        self.terminal_mode = False

        ### Private Members ###
        self._actions, self._press_actions, self._hold_actions = [], [], []
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
        if self.is_open == False:
            if self.debug_flag:
                util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")

        x = int(pygame.mouse.get_pos()[0] / self.scale)
        y = int(pygame.mouse.get_pos()[1] / self.scale)
        return (x, y)

    def set_vbuffer(self, arg1, scale=1) -> None:
        """
        Sets the vbuffer object to display on screen

        Positional Arguments:
            arg1  -- VBuffer/np.ndarray
            scale -- int/float

        Raises:
            TypeError: arg1 VBuffer/np.ndarray type check
            TypeError: scale int/float type check
        """

        if arg1 == None or (type(arg1) is not np.ndarray and type(arg1) is not VBuffer):
            raise TypeError("Argument must be of type VBuffer or np.ndarray")

        if type(scale) is not int and type(scale) is not float:
            raise TypeError("arg2 must be of type Int")

        self.vbuffer = arg1 if type(self.vbuffer) is VBuffer else VBuffer(arg1)
        self.scale = scale
        self.write_to_screen()

    def open(self, terminal_mode=False) -> None:
        """
        Creates and runs pygame window in a new thread
        """
        self.terminal_mode = terminal_mode

        if terminal_mode:
            thread = threading.Thread(target=self._start, args=(True,))
            thread.start()
        else:
            self._start(False)

    def close(self) -> None:
        """
        Closes the active instance of a pygame window

        Raises:
            RuntimeError: no active pygame window instances exists
        """

        if not self.is_open:
            if self.debug_flag:
                util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")

        self.is_open, self._screen = False, None
        pygame.quit()

    def write_to_screen(self) -> None:
        """
        Updates the screen with changes from stored vbuffer object
        """

        # swap surfaces
        self._surfaces["active"], self._surfaces["inactive"] = (
            self._surfaces["inactive"],
            self._surfaces["active"],
        )

        pygame.surfarray.blit_array(self._surfaces["active"], self.vbuffer.buffer)

        if self._screen != None and self.is_open:
            x = self.vbuffer.get_dimensions()[0] * self.scale
            y = self.vbuffer.get_dimensions()[1] * self.scale
            scaled = pygame.transform.scale(self._surfaces["active"], (x, y))

            self._screen.blit(scaled, (0, 0))
            pygame.display.flip()

    def new_action(self, func, args=None) -> None:
        """
        Creates an Action object for func to be triggered every iteration of event loop

        Positional Arguments:
            func -- function   -- function to trigger
            args -- tuple/list -- arguments to func
        """

        self._check_valid_action("a", func, args)

        function = None
        if args is not None:
            if args is not type(tuple) and args is not type(list):
                args = [args]

            function = lambda: func(*args)

        if function == None:
            function = func
        self._actions.append(Action(None, function))

    def new_press_action(self, key, func, args=None) -> None:
        """
        Creates an Action object for func to be triggered on each key press

        Positional Arguments:
            key  -- string     -- key event to trigger func
            func -- function   -- function to trigger
            args -- tuple/list -- arguments to func
        """

        self._check_valid_action(key, func, "on_press")

        function = None
        if args is not None:
            if args is not type(tuple) and args is not type(list):
                args = [args]

            function = lambda: func(*args)

        if function == None:
            function = func
        self._press_actions.append(Action(key, function))

    def new_hold_action(self, key, func, args=None) -> None:
        """
        Creates an Action object for func to be triggered when key is down

        Positional Arguments:
            key  -- string     -- key event to trigger func
            func -- function   -- function to trigger
            args -- tuple/list -- arguments to func
        """

        self._check_valid_action(key, func, "on_hold")

        function = None
        if args is not None:
            if args is not type(tuple) and args is not type(list):
                args = [args]

            function = lambda: func(*args)

        if function == None:
            function = func
        self._hold_actions.append(Action(key, function))

    def _start(self,terminal_mode) -> None:
        """
        Primary pygame window event abstraction. Opens a window and manages event loop
        """
        newx = self.vbuffer.get_dimensions()[0] * self.scale
        newy = self.vbuffer.get_dimensions()[1] * self.scale
        self._screen = pygame.display.set_mode((newx, newy))

        pygame.display.init()
        self.is_open = True
        self._build_events_dict()

        if terminal_mode:
            while self.is_open:

                for action in self._actions:
                    action.function()

                for action in self._press_actions:
                    if action.key in self.eventq:
                        action.function()

                for action in self._hold_actions:
                    if self.events[action.key]:
                        action.function()

                self.update()

    def update(self) -> None:
        """
        Pygame event abstraction, called at end of pygame loop

        Raises:
            Runtime Error: No active pygame window
        """
        if self.is_open == False:
            if self.debug_flag:
                util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")
        else:
            self.eventq.clear()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()

                self._update_events(event)

    def _update_events(self, event) -> None:
        """
        Updates the Window class event dictionary to maintain continuity with pygame events

        Positional Arguments:
            event -- current event to update
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

    def _check_valid_action(self, key, func, argname) -> None:
        """
        Typechecking before creating a new Action object

        Positional Arguments:
            key     -- string   -- key event to trigger func
            func    -- function -- function to trigger
            argname -- string   -- method name that called _check_valid_action


        Raises:
            RuntimeError: terminal_mode check
            TypeError:    key string type check
            ValueError:   key supported event type
            TypeError:    func is a valid callable function
        """
        if not terminal_mode:
            raise RuntimeError("Must be in terminal mode to create actions")
        if type(key) != str:
            raise TypeError(f"{argname} | arg1 must be of type string not {type(key)}")
        if key not in self.events:
            raise ValueError(f"{argname} | arg1 is not a valid key")
        if not callable(func):
            raise TypeError(f"{argname} | arg2 must be function not {type(func)}")
