import numpy as np
import pygame


#import os #temp
#os.environ["SDL_VIDEODRIVER"]="x11"#temp

class Window:
    
    def __init__(self):
        
        self.VisualBuffer = np.zeros((600,600))       #temp
        self.EventDictionary = {}                     #temp
        self.DebugFlag = True                         #temp
        self.Running = False                          #temp, if pygame currently active
        
    
    def GetMousePosition(self):
        return None               #temp
    
    def SetVisualBuffer(self, VisualBuffer):
        return None               #temp
    
    def Open(self):
        FRAME_WIDTH = self.VisualBuffer.shape[0]
        FRAME_HEIGHT = self.VisualBuffer.shape[1]
        FRAME = pygame.display.set_mode([FRAME_WIDTH, FRAME_HEIGHT])
        
        pygame.init()
        
        self.Running = True
        FRAME.blit(FRAME, (0, 0))
        pygame.display.update()

        pygame.display.flip()
            


    
    def Close(self):
        self.Running = False
        pygame.quit()


        

## Open Window Example (Without VisualBuffer class/event dictionary)
        
window = Window()

window.Open()

while window.Running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window.Close()



window.Close()