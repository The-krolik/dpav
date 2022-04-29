import dpav as dp

white = dp.VBuffer([1920, 1080])
white.buffer.fill(0xFFFFFF)
black = dp.VBuffer([1920, 1080])
win = dp.Window(white)
a = dp.Audio()
a.volumeLevel = 1.0

a.play_sound(5587, 11)
is_white = True
win.open()
while win.is_open():
    if is_white:
        win.set_vbuffer(black)
        is_white = False
    else:
        win.set_vbuffer(white)
        is_white = True
