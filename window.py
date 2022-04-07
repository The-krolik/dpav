import numpy as np
import pygame
import utility as util
from vbuffer import VBuffer


class Window:
    
    def __init__(self, vB=None):
        if vB != None and type(vB) is not VBuffer:
            raise TypeError("Argument must be of type VBuffer")
        
        # create buffer if not provided
        self._vB = VBuffer((800,600)) if vB == None else vB
        
        self.Events = {}
        self.ActiveEvents = []
        
        self.DebugFlag = False
        self.Screen = None
        self.isOpen = False
        

    '''
    Description:
        Returns the current mouse location with respect to the pygame window instance
    Raises:
        Runtime Error: no active pygame window instances exists
    '''
    def GetMousePosition(self):
        if self.isOpen == False:
            debug = "No window currently open"
            if self.DebugFlag:
                util._debugOut(debug)
            raise RuntimeError("No window currently open")
        
        
        return pygame.mouse.get_pos()
    
    '''
    Description:
        Sets the VBuffer object to display
    Arguments:
        vB: VBuffer object
    Raises:
        Type Error: vB must be of type VBuffer
    
    '''
    def SetVisualBuffer(self, vB):
        if vB != None and type(vB) is not VBuffer:
            raise TypeError("Argument must be of type VBuffer")
        
        self._vB = vB
        
        if self.isOpen:
            self.Screen.blit(vB, (0, 0))
            pygame.display.flip()
            
    '''
    Description:
        Primary pygame event abstraction, must be called after Open() in a process loop
    Raises:
        Runtime Error: no active pygame window instances exists
    '''
    def Update(self):
        if self.isOpen == False:
            debug = "No window currently open"
            if self.DebugFlag:
                util._debugOut(debug)
            raise RuntimeError("No window currently open")
        else:
            self.ActiveEvents.clear()
            for event in pygame.event.get():

                # if window close button is pressed (X)
                if event.type == pygame.QUIT:
                    self.Close()

                self._updateEvents(event)
    
    '''
    Description:
        Opens an instance of a pygame window
    '''
    def Open(self):
        self.isOpen = True
        self.Screen = pygame.display.set_mode(self._vB.getDimensions())
        pygame.init()
        pygame.display.flip()
        self._buildEvents()
        
    
    '''
    Description:
        Close closes the active instance of a pygame window
        
    Raises:
        RuntimeError: no active pygame window instances exists
    '''
    def Close(self):
        if not self.isOpen:
            if self.DebugFlag:
                debug = "Close() window called with no open window detected"
                util._debugOut(debug)
                
            raise RuntimeError("No window currently open")
        
        self.isOpen = False
        self.Screen = None
        pygame.quit()

        
    '''
    Description:
        updates the Window class Event dictionary to maintain continuity with pygame events
        is called for every event in the pygame events queue
        
    Arguments:
         event : current event to update
    '''
    def _updateEvents(self, event):
        
        intkey = event.type
            
        if intkey == None:
            strkey = 'None'
        elif intkey > 127 or intkey < 0:
           
            if intkey in self._keydict:
                strkey = self._keydict[intkey]
            elif self.DebugFlag:
                debug = "key pressed does not contain viable key mapping"
                util._debugOut(debug)
                
                strkey = 'None'
        else:
            strkey = chr(intkey)
            

        if strkey != 'None' and strkey in self.Events:
            self.Events[strkey] = True if self.Events[strkey] == False else False
            
            if self.Events[strkey]:
                self.ActiveEvents.append(strkey)
            
            if self.DebugFlag:
                debug = "key '{}' set to {}".format(strkey, self.Events[strkey])
                util._debugOut(debug)
            
    
    ''' 
    Description:
        creates the Events dictionary
        is called once by Open() each time a window is opened.
    '''
    def _buildEvents(self):
        
        # used for mapping of pygame keys when key isnt an ASCII character
        self._keydict = {pygame.K_F1 : 'f1', pygame.K_F2 : 'f2', pygame.K_F3 : 'f3', pygame.K_F4 : 'f4',
                        pygame.K_F5 : 'f5', pygame.K_F6 : 'f6', pygame.K_F7 : 'f7', pygame.K_F8 : 'f8',
                        pygame.K_F9 : 'f9', pygame.K_F10 : 'f10', pygame.K_F11 : 'f11', pygame.K_F12 : 'f12',
                        pygame.MOUSEBUTTONDOWN : 'mouse',
                        1073742049  : 'l_shift', 1073742053 : 'r_shift', 1073742048 : 'l_ctr', 1073742052: 'r_ctrl',
                        1073742050  : 'l_alt'  , 1073742054 : 'r_alt',   1073741881 : 'caps_lock', 
                        1073741904  : 'l_arrow', 1073741903 : 'r_arrow', 1073741905 : 'd_arrow',
                        1073741906  : 'u_arrow'
                       }
        
        # add [a-z] to dictionary
        for code in range(ord('a'), ord('z') + 1):
            self.Events[chr(code)] = pygame.key.get_pressed()[int(code)]
            
        # add [, - . /] and [0-9] to dictionary
        for code in range(ord(','), ord('9') + 1):
            self.Events[chr(code)] = pygame.key.get_pressed()[int(code)]
        
        # add non-ASCII keys to event dictionary
        for key, value in self._keydict.items():
            self.Events[value] = pygame.key.get_pressed()[key]