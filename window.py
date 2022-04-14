import numpy as np
import pygame
import utility as util
from vbuffer import VBuffer
import threading

class Action:
    def __init__(self, key, function):
        self.key = key
        self.function = function


class Window:
    
    def __init__(self, arg1=None, scale=1):
        if arg1 != None and (type(arg1) is not VBuffer and type(arg1) is not np.ndarray):
            raise TypeError("arg1 must be of type VBuffer or np.ndarray")
        if type(scale) is not int and type(scale) is not float:
            raise TypeError("arg2 must be of type Int")
        
        
        self.scale = scale
        
        # create buffer if not provided
        if arg1 == None: self.vbuffer = VBuffer((800,600))
        elif type(arg1) == VBuffer: self.vbuffer = arg1
        elif type(arg1) == np.ndarray: self.vbuffer = VBuffer(arg1)
        
        self.vbuffer = VBuffer((800,600)) if arg1 == None else arg1
        self.surfaces = {"active" : pygame.Surface(self.vbuffer.get_dimensions()), 
                         "inactive" : pygame.Surface(self.vbuffer.get_dimensions())}
        
        
        self.events = {}
        self.active_events = []
        self.press_actions = []
        self.hold_actions = []
        
        self.debug_flag = False
        self.screen = None
        self.isopen = False
        

    '''
    Description:
        Returns the current mouse location with respect to the pygame window instance
    Raises:
        Runtime Error: no active pygame window instances exists
    '''
    def get_mouse_pos(self):
        if self.isopen == False:
            if self.debug_flag: util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")
        
        
        return (int(pygame.mouse.get_pos()[0]/self.scale), int(pygame.mouse.get_pos()[1]/self.scale))
    
    '''
    Description:
        Sets the VBuffer object to display
    Arguments:
        vB: VBuffer object
    Raises:
        Type Error: vB must be of type VBuffer
    '''
    def set_vbuffer(self, arg1, scale=1):
        
        if (arg1 == None or (type(arg1) is not np.ndarray and type(arg1) is not VBuffer)):
            raise TypeError("Argument must be of type VBuffer or np.ndarray")
        
                
        if type(scale) is not int and type(scale) is not float:
            raise TypeError("arg2 must be of type Int")
        
        
        self.vbuffer = arg1 if type(self.vbuffer) is VBuffer else VBuffer(arg1)
        self.scale = scale
        self.write_to_screen()
            
    '''
    Description:
        Primary pygame event abstraction, must be called after open() in a process loop
    Raises:
        Runtime Error: no active pygame window instances exists
    '''
    def update(self):
        if self.isopen == False:
            if self.debug_flag: util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")
        else:
            self.active_events.clear()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.close()

                self.update_events(event)
                
            
    def write_to_screen(self):
        #swap surfaces
        self.surfaces['active'], self.surfaces['inactive'] = self.surfaces['inactive'], self.surfaces['active']
        pygame.surfarray.blit_array(self.surfaces['active'], self.vbuffer.buffer)
        
        if self.screen != None and self.isopen:
            self.screen.blit(pygame.transform.scale(self.surfaces['active'], (self.vbuffer.get_dimensions()[0] * self.scale, self.vbuffer.get_dimensions()[1] * self.scale)), (0, 0))
            pygame.display.flip()
    
    '''
    Description:
        opens an instance of a pygame window
    '''

    def open(self, *args):
        thread = threading.Thread(target=self._start)
        thread.start()
        
        
    def _start(self):
        self.screen = pygame.display.set_mode((self.vbuffer.get_dimensions()[0] * self.scale, self.vbuffer.get_dimensions()[1] * self.scale))
        pygame.display.init()
        self.isopen = True
        self.write_to_screen()
        self._build_events_dict()
        
        while self.isopen:
            
            for action in self.press_actions:
                if action.key in self.active_events:
                    action.function()
            
            for action in self.hold_actions:
                if self.events[action.key]:
                    action.function()
            
            self.update()
        
    def _check_valid_action(self,key,func,argname):
        
        if type(key) != str:
            raise TypeError(f"{argname} | arg1 must be of type string not {type(key)}")
        if not callable(func):
            raise TypeError(f"{argname} | arg2 must be function not {type(func)}")
        
        
    
    def on_press(self, key,func, args=None):
        self._check_valid_action(key,func,"on_press")
        
        function = None
        if args is not None:
            if args is not type(tuple) and args is not type(list):
                args = [args]
            
            function = lambda : func(*args)
        
        if function == None: function = func
        self.press_actions.append(Action(key,function))
        
    def on_hold(self, key,func, args=None):
        self._check_valid_action(key,func,"on_hold")
        
        function = None
        if args is not None:
            if args is not type(tuple) and args is not type(list):
                args = [args]
                
            function = lambda : func(*args)
        
        if function == None: function = func
        self.hold_actions.append(Action(key,function))
        
        

        
    '''
    Description:
        Closes the active instance of a pygame window   
    Raises:
        RuntimeError: no active pygame window instances exists
    '''
    def close(self):
        if not self.isopen:
            if self.debug_flag: util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")
        
        self.isopen, self.screen = False, None
        pygame.quit()

        
        
    '''
    Description:
        updates the Window class Event dictionary to maintain continuity with pygame events
        is called for every event in the pygame events queue
    Arguments:
         event : current event to update
    '''
    def update_events(self, event):
        strkey = 'None'
        
        #if mouse, intkey = event.type, else set to pygame key value
        intkey = event.dict.get('key') if event.type in [768,769] else event.type
        
        if intkey == None: strkey = 'None'
        elif intkey in self._keydict: strkey = self._keydict[intkey]
            
        
        if strkey != 'None' and strkey in self.events:
            self.events[strkey] = True if self.events[strkey] == False else False
            
            if self.events[strkey]: self.active_events.append(strkey)
            if self.debug_flag: util._debugOut("key '{}' set to {}".format(strkey, self.events[strkey]))
        
        
    
    ''' 
    Description:
        creates the events dictionary
        is called once by open() each time a window is opened.
    '''
    def _build_events_dict(self):
        
        # used for mapping of pygame key int identifiers to string identifiers
        self._keydict = {pygame.K_F1 : 'f1', pygame.K_F2 : 'f2', pygame.K_F3 : 'f3', pygame.K_F4 : 'f4',
                        pygame.K_F5 : 'f5', pygame.K_F6 : 'f6', pygame.K_F7 : 'f7', pygame.K_F8 : 'f8',
                        pygame.K_F9 : 'f9', pygame.K_F10 : 'f10', pygame.K_F11 : 'f11', pygame.K_F12 : 'f12',
                        pygame.MOUSEBUTTONDOWN : 'mouse', pygame.MOUSEBUTTONUP: 'mouse',
                        1073742049  : 'l_shift', 1073742053 : 'r_shift', 1073742048 : 'l_ctr', 1073742052: 'r_ctrl',
                        1073742050  : 'l_alt'  , 1073742054 : 'r_alt',   1073741881 : 'caps_lock', 
                        1073741904  : 'l_arrow', 1073741903 : 'r_arrow', 1073741905 : 'd_arrow',
                        1073741906  : 'u_arrow'
                       }
        
        # add [a-z] to dict
        for code in range(ord('a'), ord('z') + 1): self._keydict[code] = chr(code)
            
        # add [, - . /] and [0-9] to dict
        for code in range(ord(','), ord('9') + 1): self._keydict[code] = chr(code)
        
        # create events dict from _keydict string mappings
        for key, value in self._keydict.items(): self.events[value] = pygame.key.get_pressed()[key]
        
        
        
