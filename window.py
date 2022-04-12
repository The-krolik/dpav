import numpy as np
import pygame
import utility as util
from vbuffer import VBuffer


class Window:
    
    def __init__(self, vB=None):
        if vB != None and type(vB) is not VBuffer:
            if self.debugFlag: util._debugOut("Argument must be of type VBuffer")
            raise TypeError("Argument must be of type VBuffer")
        
        # create buffer if not provided
        self.vBuffer = VBuffer((800,600)) if vB == None else vB
        self.surfaces = {"active" : pygame.Surface(self.vBuffer.getDimensions()), 
                         "inactive" : pygame.Surface(self.vBuffer.getDimensions())}
        
        
        self.events = {}
        self.activeEvents = []
        
        self.debugFlag = False
        self.screen = None
        self.isOpen = False
        

    '''
    Description:
        Returns the current mouse location with respect to the pygame window instance
    Raises:
        Runtime Error: no active pygame window instances exists
    '''
    def getMousePosition(self):
        if self.isOpen == False:
            if self.debugFlag: util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")
        
        
        return pygame.mouse.get_pos()
    
    '''
    Description:
        Sets the VBuffer object to display
    Arguments:
        vB: VBuffer object
    Raises:
        TypeError: vB must be of type VBuffer
    '''
    def setVBuffer(self, vB):
        if vB != None and type(vB) is not VBuffer:
            if self.debugFlag: util._debugOut("Arg to setVBuffer must be of type VBuffer")
            raise TypeError("Arg to setVBuffer must be of type VBuffer")
        
        self.vBuffer = vB
        self.writeToScreen()
            
    '''
    Description:
        Primary pygame event abstraction, must be called after open() in a process loop
    Raises:
        RuntimeError: no active pygame window instances exists
    '''
    def update(self):
        #self.writeToScreen()
        
        
        if self.isOpen == False:
            if self.debugFlag: util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")
        else:
            self.activeEvents.clear()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.close()

                self._updateEvents(event)
                
            
    def writeToScreen(self):
        #swap surfaces
        self.surfaces['active'], self.surfaces['inactive'] = self.surfaces['inactive'], self.surfaces['active']
        pygame.surfarray.blit_array(self.surfaces['active'], self.vBuffer.buffer)
        
        if self.screen != None and self.isOpen:
            self.screen.blit(self.surfaces['active'], (0, 0))
            pygame.display.flip()
    
    '''
    Description:
        opens an instance of a pygame window
    '''
    def open(self):
        self.screen = pygame.display.set_mode(self.vBuffer.getDimensions())
        pygame.display.init()
        self.isOpen = True
        self.writeToScreen()
        self._buildEventsDict()

    '''
    Description:
        Closes the active instance of a pygame window   
    Raises:
        RuntimeError: no active pygame window instances exists
    '''
    def close(self):
        if not self.isOpen:
            if self.debugFlag: util._debugOut("No window currently open")
            raise RuntimeError("No window currently open")
        
        self.isOpen, self.Screen = False, None
        pygame.quit()

        
        
    '''
    Description:
        updates the Window class Event dictionary to maintain continuity with pygame events
        is called for every event in the pygame events queue
    Arguments:
         event : current event to update
    '''
    def _updateEvents(self, event):
        strkey = 'None'
        
        #if mouse, intkey = event.type, else set to pygame key value
        intkey = event.dict.get('key') if event.type in [768,769] else event.type
        
        if intkey == None: strkey = 'None'
        elif intkey in self._keydict: strkey = self._keydict[intkey]
            
        
        if strkey != 'None' and strkey in self.events:
            self.events[strkey] = True if self.events[strkey] == False else False
            
            if self.events[strkey]: self.activeEvents.append(strkey)
            if self.debugFlag: util._debugOut("key '{}' set to {}".format(strkey, self.events[strkey]))
        
        
    
    ''' 
    Description:
        creates the events dictionary
        is called once by open() each time a window is opened.
    '''
    def _buildEventsDict(self):
        
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