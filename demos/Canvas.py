import dypi

vb = dypi.VBuffer([50, 50])
vb[:] = 0xFFFFFF
window = dypi.Window(vb, 12)

window.open()
color = 0x000000
while window.is_open():
    if "w" in window.eventq:
        color = 0xFFFFFF
    elif "r" in window.eventq:
        color = 0xFF0000
    elif "o" in window.eventq:
        color = 0xFFA500
    elif "y" in window.eventq:
        color = 0xFFFF00
    elif "g" in window.eventq:
        color = 0x00FF00
    elif "f" in window.eventq:
        vb[:] = color
    elif "b" in window.eventq:
        color = 0x0000FF
    elif "i" in window.eventq:
        color = 0x4B0082
    elif "v" in window.eventq:
        color = 0x8F00FF
    elif "0" in window.eventq:
        color = 0x000000
    elif "-" in window.eventq:
        vb.clear()
    elif "," in window.eventq:
        vb.save_buffer_to_file("pic")
    elif "." in window.eventq:
        vb.load_buffer_from_file("pic")

    if window.events["mouse"]:
        pos = window.get_mouse_pos()
        vb[pos] = color
