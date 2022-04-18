import numpy as np
import directpythonplatform as dpp

def coord_in_set(c_arg, start_z, itr=20):
    c = complex(*c_arg)
    z = complex(*start_z)

    for i in range(itr):
        try:
            if abs(z) < 1000:
                z = z**2 + c
            else:
                return min(0x0000ff, 0x000011 * i)
                
        except OverflowError:
            return 0x0000ff

    try:
        if abs(z) < 2:
            return 0
        else:
            return 0x000011
    except OverflowError:
        return 0x0000ff

def transform_position(two_tuple, original_dim):
    new_dim = 4.5
    factor = (new_dim/original_dim)
    d1 = two_tuple[0] * factor
    d2 = two_tuple[1] * factor
    d1 -= new_dim / 2
    d2 -= new_dim / 2

    d2 *= -1
    return (d1, d2)

def out_of_bounds(c, lim):
    if c is None:
        return True
    x = c[0]
    y = c[1]
    if x < 0 or x > lim:
        return True
    if y < 0 or y > lim:
        return True
    return False

def julia_loop():
    DIM = 500
    shape = (DIM, DIM)
    startb = dpp.VBuffer(shape)
    
    window = dpp.Window(startb)

    window.open()
    while window.is_open():
        nextb = dpp.VBuffer(shape)
        raw_position = None
        while out_of_bounds(raw_position, DIM):
            raw_position = window.get_mouse_pos()
        julia_starter = transform_position(raw_position, DIM)
        for y in range(nextb.get_dimensions()[0]):
            for x in range(nextb.get_dimensions()[1]):
                cur_pos = transform_position((x, y), DIM)
                color = coord_in_set(julia_starter, cur_pos)
                nextb.write_pixel((x, y), color)
        window.set_vbuffer(nextb)

def mandelbrot_loop():
    DIM = 500
    shape = (DIM, DIM)
    startb = dpp.VBuffer(shape)
    
    window = dpp.Window(startb)

    window.open()
    constructed = False
    while window.is_open():
        if not constructed:
            nextb = dpp.VBuffer(shape)
            for y in range(nextb.get_dimensions()[0]):
                for x in range(nextb.get_dimensions()[1]):
                    cur_pos = transform_position((x, y), DIM)
                    color = coord_in_set(cur_pos, (0, 0), 50)
                    nextb.write_pixel((x, y), color)
            window.set_vbuffer(nextb)
        constructed = True
    

def main():
    x = 1
    while True:
        print("Do you want a julia set or a mandelbrot set?")
        x = input("1: Julia set\n2: Mandelbrot set\nAnything Else: Quit\n==> ")
        if x == "1":
            julia_loop()
        elif x == "2":
            mandelbrot_loop()
        else:
            break

main()
