import dpav as dp

white = dp.VBuffer([1920, 1080])
white.buffer.fill(0xFFFFFF)
black = dp.VBuffer([1920, 1080])
win = dp.Window(white)
a = dp.Audio()
a.volumeLevel = 1.0

a.playSound(5587, 11)
win.open()
while win.isOpen:
    win.setVBuffer(black)
    win.update()
    win.setVBuffer(white)
    win.update()
