import numpy as np
import pygame
from visual import Visual


import os #temp
os.environ["SDL_VIDEODRIVER"]="x11"#temp

class Window:
    
    def __init__(self, vB=None):
        
        self.VB = vB
        self.EventDictionary = {}
        self.DebugFlag = True
        
        self.Screen = None
        self.isOpen = False
        

    def GetMousePosition(self):
        return pygame.mouse.get_pos()
    
    def SetVisualBuffer(self, vB):
        self.VB = vB
        
        if self.isOpen:
            self.Screen.blit(VB, (0, 0))
            pygame.display.flip()
    
    
    def Update(self):
        
        for event in pygame.event.get():
            # if window claose button is pressed (X)
            if event.type == pygame.QUIT:
                window.Close()
                
            self._updateEventDictionary(event)
    
    def Open(self):
        self.isOpen = True
        
        self.Screen = pygame.display.set_mode(self.VB.getDimensions())
        pygame.init()
        pygame.display.flip()
        
        self._buildEventDictionary()
        
    
    def Close(self):
        self.isOpen = False
        pygame.quit()


    def _updateEventDictionary(self, event):
        
        intkey = event.dict.get('key')
            
        if intkey == None:
            strkey = 'None'
        elif intkey > 127 or intkey < 0:
            if intkey in self._keydict:
                strkey = self._keydict[intkey] #temp
            else:
                print(intkey)
                strkey = 'None'
        else:
            strkey = chr(intkey)
            

        if strkey != 'None' and strkey in self.EventDictionary:
                
            # if key state is True, set to False if False set to True
            self.EventDictionary[strkey] = True if self.EventDictionary[strkey] == False else False
    
    def _buildEventDictionary(self):
        
        # used for mapping of pygame keys when key isnt an ASCII character
        self._keydict = {pygame.K_F1 : 'f1', pygame.K_F2 : 'f2', pygame.K_F3 : 'f3', pygame.K_F4 : 'f4',
                        pygame.K_F5 : 'f5', pygame.K_F6 : 'f6', pygame.K_F7 : 'f7', pygame.K_F8 : 'f8',
                        pygame.K_F9 : 'f9', pygame.K_F10 : 'f10', pygame.K_F11 : 'f11', pygame.K_F12 : 'f12',
                        1073742049  : 'l_shift', 1073742053 : 'r_shift', 1073742048 : 'l_ctr', 1073742052: 'r_ctrl',
                        1073742050  : 'l_alt'  , 1073742054 : 'r_alt',   1073741881 : 'caps_lock', 
                        1073741904  : 'l_arrow', 1073741903 : 'r_arrow', 1073741905 : 'd_arrow',
                        1073741906  : 'u_arrow'
                       }
        
        # add [a-z] to dictionary
        for code in range(ord('a'), ord('z') + 1):
            self.EventDictionary[chr(code)] = pygame.key.get_pressed()[int(code)]
            
        # add [, - . /] and [0-9] to dictionary
        for code in range(ord(','), ord('9') + 1):
            self.EventDictionary[chr(code)] = pygame.key.get_pressed()[int(code)]
        
        # add non-ASCII keys to event dictionary
        for key, value in self._keydict.items():
            self.EventDictionary[value] = pygame.key.get_pressed()[key]
        
        

## Open Window Example w/ Event Dictionary

buffer = Visual(600,600)
window = Window(buffer)

window.Open()
while window.isOpen:
    window.Update()
    
    if window.EventDictionary['a']:
        print("'A' Key Pressed")



# TODO: Debug Log

#UTILITY FUNCTION TODO:
#   Queue Events