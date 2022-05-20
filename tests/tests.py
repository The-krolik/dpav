import pytest
import dpav as dp
import sdl2
from typing import Type


def test_audio():
    a = dp.Audio()

    assert a.get_bit_number() == 16
    assert a.get_sample_rate() == 44100
    assert a.waveform == a.waves.sin

    a.set_waveform(a.waves.square)
    assert a.waveform == a.waves.square

    with pytest.raises(Exception) as e_info:
        a.set_waveform(a.waves.cos)
    assert a.waveform == a.waves.square


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
    x, y = vb.dimensions
    assert x == 800
    assert y == 600

    vb = dp.VBuffer(1920, 1080)
    x, y = vb.dimensions
    assert x == 1920
    assert y == 1080

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
        vb.surface = sdl2.SDL_Surface

# def test_set_buffer():
# def test_buffer_files():
