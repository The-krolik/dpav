import numpy as np
import pygame
from visual import Visual


import os #temp
os.environ["SDL_VIDEODRIVER"]="x11"#temp

class Window:
    
    def __init__(self, vB=None):
        
        
        self.VB = vB                                  #temp
        self.EventDictionary = {}                     #temp
        self.DebugFlag = True                         #temp
        
        self.Screen = None
        self.isOpen = False                          #temp, if pygame currently active
        
        
        
    
    def GetMousePosition(self):
        return pygame.mouse.get_pos()
    
    def SetVisualBuffer(self, vB):
        self.VB = vB
        
        if self.Open:
            self.Screen.blit(VB, (0, 0))
            pygame.display.flip()
    
    
    def Open(self):
        self.isOpen = True
        
        self.Screen = pygame.display.set_mode(self.VB.getDimensions())
        pygame.init()
        pygame.display.flip()
        
    
    def Close(self):
        self.isOpen = False
        pygame.quit()


        

## Open Window Example (Without VisualBuffer class/event dictionary)

buffer = Visual(600,600)
window = Window(buffer)

window.Open()

while window.isOpen:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window.Close()



window.Close()