from window import Window

window = Window()
window.DebugFlag = True

window.Open()
while window.isOpen:
    window.Update()
    
    if window.EventDictionary['a']:
        print("'A' Key Pressed")
