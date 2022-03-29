import numpy as np
import pygame

class Window:
    
    def __init__(self):
        
        VisualBuffer = None
        EventDictionary = None
        DebugFlag = None
		Screen = None
           
    def GetMousePosition(self):
        return pygame.mouse.get_pos()
    
    def SetVisualBuffer(self, VisualBuffer):
        VisualBuffer = VisualBuffer
    
    def Open(width, height):
        Screen = pygame.display.set_mode((width, height))
		VisualBuffer = VisualBuffer(width, height)
    
    def Close(self):
        pygame.display.quit()