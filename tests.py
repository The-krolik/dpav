import pytest
import directpythonplatform as dpp
from typing import Type


def test_audio():
    a = dpp.Audio()

    assert a.getBitNumber() == 16
    assert a.getSampleRate() == 44100   
    assert a.waveform == a.waves.sin

    a.setWaveForm(a.waves.square)
    assert a.waveform == a.waves.square

    with pytest.raises(Exception) as e_info:
        a.setWaveForm(a.waves.cos)
    assert a.waveform == a.waves.square


def test_vbuffer():
    vb = dpp.VBuffer()
    x, y = vb.getDimensions()
    assert x > 0
    assert y > 0
    assert type(x) is int
    assert type(y) is int

    with pytest.raises(ValueError) as e_info:
        vb = dpp.VBuffer([0, 0])

    with pytest.raises(ValueError) as e_info:
        vb = dpp.VBuffer([0, 600])

    with pytest.raises(ValueError) as e_info:
        vb = dpp.VBuffer([800, 0])

    with pytest.raises(ValueError) as e_info:
        vb = dpp.VBuffer([9999, 9999])

    with pytest.raises(ValueError) as e_info:
        vb = dpp.VBuffer([-100, -100])

    with pytest.raises(TypeError) as e_info:
        vb = dpp.VBuffer([100.9, 200])

    with pytest.raises(TypeError) as e_info:
        vb = dpp.VBuffer([200, 200.5])

    vb = dpp.VBuffer([1920, 1080])
    x, y = vb.getDimensions()
    assert type(x) is int
    assert type(y) is int
    assert x == 1920
    assert y == 1080

    vb = dpp.VBuffer()
    x, y = vb.getDimensions()
    assert type(x) is int
    assert type(y) is int
    assert x == 800
    assert y == 600

    vb = dpp.VBuffer([800, 600])
    assert vb.getPixel([400, 300]) == 0

    with pytest.raises(ValueError) as e_info:
        vb.writePixel([-300, 9], 16777215)

    with pytest.raises(ValueError) as e_info:
        vb.writePixel([300, -200], 16777215)

    with pytest.raises(TypeError) as e_info:
        vb.writePixel([300.1, 200], 16777215)

    with pytest.raises(TypeError) as e_info:
        vb.writePixel([20, 799.5], 16777215)

    with pytest.raises(ValueError) as e_info:
        vb.writePixel([399, 299], 16777216)
    assert vb.getPixel([399, 299]) == 0

    with pytest.raises(ValueError) as e_info:
        vb.writePixel([399, 299], -1)
    assert vb.getPixel([399, 299]) == 0

    with pytest.raises(TypeError) as e_info:
        vb.writePixel([399, 299], 100.5)
    assert vb.getPixel([399, 299]) == 0

    vb.writePixel([0, 0], 16777215)
    assert vb.getPixel([0, 0]) == 16777215

    vb.writePixel([799, 599], 0xffffff)
    assert vb.getPixel([0, 0]) == 16777215

    vb.clearBuffer()
    assert vb.buffer.sum() == 0
