import pytest
import sdl2
import numpy as np
from typing import Type
import dpav as dp

def test_arr_init():
    arr = np.zeros((750, 550))
    arr[:] = 0x00FF00
    vb = dp.VBuffer(arr)
    assert vb.dimensions == (750, 550)
    failed = False
    for i in len(vb):
        for j in len(vb[i]):
            if vb[i, j] != 0x00FF00:
                failed = True
    assert failed == False

def test_dimensions():
    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer(0, 0)
    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer(-1, 0)
    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer(0, -1)
    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer(-1, -1)

    vb = dp.VBuffer()
    assert vb.dimensions == (800, 600)

    vb = dp.VBuffer(1920, 1080)
    assert vb.dimensions == (1920, 1080)

    with pytest.raises(AttributeError) as e_info:
        vb.dimensions = (20, 20)


def test_pixel_val_init():
    vb = dp.VBuffer()
    assert vb.sum() == 0


def test_pixel_access():
    vb = dp.VBuffer()

    # what about 0xFF00FFFF?
    # vb[10, 10] = -5 needs consideration

    vb[400, 300] = 0xFF0000
    assert vb[400, 300] == 0xFF0000

    assert len(vb) = 800
    assert len(vb[0]) = 600


def test_clear():
    vb = dp.VBuffer()
    vb[:] = 0xFF0000
    vb.clear()
    assert vb.sum() == 0

def test_surface_access():
    vb = dp.VBuffer()
    with pytest.raises(AttributeError) as e_info:
        vb._surface = sdl2.SDL_Surface

    surf = vb._surface

# def test_buffer_files():
