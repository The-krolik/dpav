import numpy as np
import directpythonplatform as dpp

DIM = 500 # Const

def coord_in_set(c_arg, start_z, itr=50):
    """Return color based on coordinates and iterative equation z = z^2 + c.
    if complex number z approaches zero as equation is iterated,
    it is in the set, and is colored black. If it grows without limit, color
    based on rate at which it grows to infinity."""
    c = complex(*c_arg)
    z = complex(*start_z)
    try:
        for i in range(itr):
            if abs(z) < 1000:
                z = z**2 + c
            else:
                return min(0x0000ff, 0x000011 * i)
        if abs(z) < 2:
            return 0
        else:
            return 0x0000ff
    except OverflowError:
        return 0x0000ff

def transform_position(two_tuple):
    """Translate and scale discreet pixel coords to
    continous cartesian plane coords"""
    new_dim = 4.5
    factor = (new_dim/DIM)
    d1 = two_tuple[0] * factor
    d2 = two_tuple[1] * factor
    d1 -= new_dim / 2
    d2 -= new_dim / 2

    d2 *= -1
    return (d1, d2)

def out_of_bounds(c):
    """Check if pixel coordinate is within buffer range."""
    if c is None:
        return True
    x = c[0]
    y = c[1]
    if x < 0 or x > DIM:
        return True
    if y < 0 or y > DIM:
        return True
    return False

def get_current_c(window):
    """Get mouse position and return it as certesian coordinates, to be used
    as c in z = z^2 + c."""
    raw_position = None
    while out_of_bounds(raw_position):
        raw_position = window.get_mouse_pos()
    return transform_position(raw_position)

def calculate_pixel_colors(c):
    """Construct buffer with pixels colored based on fractal formula
    z = z^2 + c."""
    nextb = dpp.VBuffer((DIM, DIM))
    for y in range(nextb.get_dimensions()[0]):
        for x in range(nextb.get_dimensions()[1]):
            cur_pos = transform_position((x, y))
            if c is not None:
                # Calculate julia set
                color = coord_in_set(c, cur_pos)
            else:
                # Calculate mandelbrot set
                color = coord_in_set(cur_pos, (0, 0))
            nextb.write_pixel((x, y), color)
    return nextb

def fractal_loop(mode):
    """Draw and display julia set or mandelbrot set."""
    startb = dpp.VBuffer((DIM, DIM))
    
    window = dpp.Window(startb)

    window.open()
    mandelbrot_constructed = False
    while window.is_open():
        if mandelbrot_constructed and mode == "mandelbrot":
            continue
        
        if mode == "julia":
            c = get_current_c(window)
        else:
            c = None
            
        nextbuf = calculate_pixel_colors(c)
        
        window.set_vbuffer(nextbuf)
        mandelbrot_constructed = True
    

def main():
    x = 1
    while True:
        print("Do you want a julia set or a mandelbrot set?")
        x = input("1: Julia set\n2: Mandelbrot set\nAnything Else: Quit\n==> ")
        if x == "1":
            fractal_loop('julia')
        elif x == "2":
            fractal_loop('mandelbrot')
        else:
            break

main()
