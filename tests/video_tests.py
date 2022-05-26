import pytest
import sdl2
import numpy as np
from typing import Type
import dpav as dp


def test_arr_init():
    test_arr = np.full((750, 550), 0x00FF00)
    vb = dp.VBuffer(test_arr)
    assert vb.dimensions == (750, 550)
    for i in range(len(vb)):
        for j in range(len(vb[i])):
            assert vb[i, j] == 0x00FF00


def test_init():
    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer((0, 0))
    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer((-1, 0))
    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer((0, -1))
    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer((-1, -1))

    vb = dp.VBuffer()
    assert vb.dimensions == (800, 600)

    vb = dp.VBuffer((1920, 1080))
    assert vb.dimensions == (1920, 1080)


def test_set_dimensions():
    vb = dp.VBuffer()
    with pytest.raises(AttributeError) as e_info:
        vb.dimensions = (20, 20)


def test_pixel_val_init():
    vb = dp.VBuffer()
    for i in range(len(vb)):
        for j in range(len(vb[i])):
            assert vb[i, j] == 0


def test_pixel_access():
    vb = dp.VBuffer()
    vb[400, 300] = 0xFF0000
    assert vb[400, 300] == 0xFF0000


def test_len():
    vb = dp.VBuffer()
    assert len(vb) == 800
    assert len(vb[0]) == 600


def test_clear():
    vb = dp.VBuffer()
    vb[:] = 0xFF0000
    vb.clear()
    for i in range(len(vb)):
        for j in range(len(vb[i])):
            assert vb[i, j] == 0


def test_surface_access():
    vb = dp.VBuffer()
    with pytest.raises(AttributeError) as e_info:
        vb.surface = sdl2.SDL_Surface

    surf = vb._surface


# def test_buffer_files():
