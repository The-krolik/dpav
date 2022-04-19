import directpythonplatform as dpp

# import threading

white = dpp.VBuffer([1920, 1080])
white.buffer.fill(0xFFFFFF)
black = dpp.VBuffer([1920, 1080])
win = dpp.Window(white)
a = dpp.Audio()
a.volumeLevel = 1.0

# def ring():
#    a = dpp.Audio()
#    a.volumeLevel = 1.0
#    a.playSound(5587, 11)
#    while a.volumeLevel != 0.0:
#        sleep(1)
#        a.volumeLevel -= .1

# thread = threading.Thread(target=ring)
# thread.start()

a.playSound(5587, 11)
win.open()
while win.isOpen:
    win.setVBuffer(black)
    win.update()
    win.setVBuffer(white)
    win.update()
