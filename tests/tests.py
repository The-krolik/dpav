import pytest
import dypi as dp
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


def test_vbuffer():
    vb = dp.VBuffer()
    x, y = vb.get_dimensions()
    assert x > 0
    assert y > 0
    assert type(x) is int
    assert type(y) is int

    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer([0, 0])

    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer([0, 600])

    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer([800, 0])

    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer([9999, 9999])

    with pytest.raises(ValueError) as e_info:
        vb = dp.VBuffer([-100, -100])

    with pytest.raises(TypeError) as e_info:
        vb = dp.VBuffer([100.9, 200])

    with pytest.raises(TypeError) as e_info:
        vb = dp.VBuffer([200, 200.5])

    vb = dp.VBuffer([1920, 1080])
    x, y = vb.get_dimensions()
    assert type(x) is int
    assert type(y) is int
    assert x == 1920
    assert y == 1080

    vb = dp.VBuffer()
    x, y = vb.get_dimensions()
    assert type(x) is int
    assert type(y) is int
    assert x == 800
    assert y == 600

    vb = dp.VBuffer([800, 600])
    assert vb.get_pixel([400, 300]) == 0

    with pytest.raises(ValueError) as e_info:
        vb.write_pixel([-300, 9], 16777215)

    with pytest.raises(ValueError) as e_info:
        vb.write_pixel([300, -200], 16777215)

    with pytest.raises(TypeError) as e_info:
        vb.write_pixel([300.1, 200], 16777215)

    with pytest.raises(TypeError) as e_info:
        vb.write_pixel([20, 799.5], 16777215)

    with pytest.raises(ValueError) as e_info:
        vb.write_pixel([399, 299], 16777216)
    assert vb.get_pixel([399, 299]) == 0

    with pytest.raises(ValueError) as e_info:
        vb.write_pixel([399, 299], -1)
    assert vb.get_pixel([399, 299]) == 0

    with pytest.raises(TypeError) as e_info:
        vb.write_pixel([399, 299], 100.5)
    assert vb.get_pixel([399, 299]) == 0

    vb.write_pixel([0, 0], 16777215)
    assert vb.get_pixel([0, 0]) == 16777215

    vb.write_pixel([799, 599], 0xFFFFFF)
    assert vb.get_pixel([0, 0]) == 16777215

    vb.clear()
    assert vb.buffer.sum() == 0
