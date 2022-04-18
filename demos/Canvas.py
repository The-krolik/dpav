import directpythonplatform as dpp

vb = dpp.VBuffer([50, 50])
window = dpp.Window(vb, 10)

window.open()
color = 0xFFFFFF
while window.is_open():
    if 'w' in window.eventq:
        color = 0xFFFFFF
    elif 'r' in window.eventq:
        color = 0xFF0000
    elif 'o' in window.eventq:
        color = 0xFFA500
    elif 'g' in window.eventq:
        color = 0x00FF00
    elif 'b' in window.eventq:
        color = 0x0000FF
    elif 'i' in window.eventq:
        color = 0x4B0082
    elif 'v' in window.eventq:
        color = 0x8F00FF
    elif '0' in window.eventq:
        color = 0x000000
    elif '1' in window.eventq:
        vb.save_buffer_to_file("pic")
    elif '2' in window.eventq:
        vb.load_buffer_from_file("pic")

    if window.events['mouse']:
        pos = window.get_mouse_pos()
        vb[pos] = color
