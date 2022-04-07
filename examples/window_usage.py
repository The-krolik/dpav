from window import Window
from vbuffer import VBuffer

buf = VBuffer((600,400))
window = Window(buf)
window.debugFlag = True

window.open()

color = 127
while window.isOpen:
    
    window.update()
    
    if 'mouse_down' in window.activeEvents:
        pos = window.getMousePosition()
        window.vBuffer.writePixel(pos,color)
        
