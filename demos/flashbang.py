import dypi

white = dypi.VBuffer([1920, 1080])
white.buffer.fill(0xFFFFFF)
black = dypi.VBuffer([1920, 1080])
win = dypi.Window(white)
a = dypi.Audio()
a.volumeLevel = 1.0

a.playSound(5587, 11)
win.open()
while win.isOpen:
    win.setVBuffer(black)
    win.update()
    win.setVBuffer(white)
    win.update()
