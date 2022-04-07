import pytest
import directpythonplatform as dpp
from typing import Type

def test_audio():
    a = dpp.Audio()


    # bit number tests
    assert a.getBitNumber() == 16

    a.setBitNumber(8)
    assert a.getBitNumber() == 8

    a.setBitNumber(32)
    assert a.getBitNumber() == 32

    with pytest.raises(Exception) as e_info:
        a.setBitNumber(33)
    assert a.getBitNumber() == 32
        
    with pytest.raises(Exception) as e_info:
        a.setBitNumber(-1)
    assert a.getBitNumber() == 32


    # sample rate tests
    assert a.getSampleRate() == 44100

    # Are other sample rates supported?


    # audio buffer tests


    a.setAudioDevice(1)
    assert a.getAudioDevice == 1

    with pytest.raises(Exception) as e_info:
        a.setAudioDevice(-1)
    assert a.getAudioDevice == 1
    
    with pytest.raises(Exception) as e_info:
        a.setAudioDevice(1.5)
    assert a.getAudioDevice == 1


    # playSound tests
    

def test_vbuffer():
    vb = dpp.VBuffer()
    x, y = vb.getDimensions()
    assert x > 0
    assert y > 0
    assert type(x) is int
    assert type(y) is int

    with pytest.raises(Exception) as e_info:
        vb = dpp.VBuffer([-100, -100])
        
    with pytest.raises(Exception) as e_info:
        vb = dpp.VBuffer([100.9, 200])
        
    with pytest.raises(Exception) as e_info:
        vb = dpp.VBuffer([200, 200.5])
        
    vb = dpp.VBuffer([800, 600])
    x, y = vb.getDimensions()
    assert type(x) is int
    assert type(y) is int
    assert x == 800
    assert y == 600

    vb = dpp.VBuffer([800, 600])
    assert vb.getPixel([400, 300]) == 0
    
    with pytest.raises(Exception) as e_info:
        vb.writePixel([-300, 9], 16777215)
    
    with pytest.raises(Exception) as e_info:
        vb.writePixel([300, -200], 16777215)
        
    with pytest.raises(Exception) as e_info:
        vb.writePixel([300.1, 200], 16777215)
        
    with pytest.raises(Exception) as e_info:
        vb.writePixel([20, 799.5], 16777215)
    
    with pytest.raises(Exception) as e_info:
        vb.writePixel([399, 299], 16777216)
    assert vb.getPixel([399, 299]) == 0

    with pytest.raises(Exception) as e_info:
        vb.writePixel([399, 299], 100.5)
    assert vb.getPixel([399, 299]) == 0

    vb.writePixel([0,0], 16777215)
    assert vb.getPixel([0, 0]) == 16777215
    
    vb.writePixel([599, 799], 0xffffff)
    assert vb.getPixel([0, 0]) == 16777215
    
    vb.clearBuffer()
    assert vb.getPixel([0,0]) == 0
