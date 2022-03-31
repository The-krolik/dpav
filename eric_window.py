import numpy as np
import pygame

class Window:
    
    def __init__(self):
        self.VB = np.zeros((600,600), 3)			# Temporary until VB class finished
        self.EventDictionary = None
        self.DebugFlag = None
		self.Screen = None
		self.Open = False
           
    def GetMousePosition(self):
        return pygame.mouse.get_pos()
    
    def SetVisualBuffer(self, VisualBuffer):
        self.VB = VisualBuffer
		if self.Open:
			self.Screen.blit(VB, (0, 0))
			pygame.display.flip()
    
    def Open(self):
		self.Open = True
		
        self.Screen = pygame.display.set_mode(self.VB.getDimensions())
		pygame.init()
		
		pygame.display.flip()
    
    def Close(self):
		self.Open = False
        pygame.display.quit()