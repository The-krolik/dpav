import directpythonplatform as dpp

def test_audio():
    a = dpp.Audio()


    # bit number tests
    assert a.getBitNumber() == 16

    a.setBitNumber(8)
    assert a.getBitNumber() == 8

    a.setBitNumber(32)
    assert a.getBitNumber() == 32

    a.setBitNumber(33)
    assert a.getBitNumber() == 8


    # sample rate tests
    assert a.getSampleRate() == 44100

    # Are other sample rates supported?


    # audio buffer tests


    # audio device tests
    a.setAudioDevice(1)
    assert a.getAudioDevice == 1

    a.setAudioDevice(-1)
    assert a.getAudioDevice == 1

    a.setAudioDevice(9999)
    assert a.getAudioDevice == 1


    # playSound tests
    

def test_vbuffer():
    vb = dpp.VBuffer()
    x, y = vb.getDimensions()
    assert x > 0
    assert y > 0

    vb = dpp.VBuffer([-100, -100])
    assert x > 0
    assert y > 0

    vb = dpp.VBuffer([800, 600])
    x, y = vb.getDimensions()
    assert x == 800
    assert y == 600

    assert vb.getPixel([400, 300]) == hex(0)

    vb.writePixel([399, 299], hex(999999999))
    assert vb.getPixel([399, 299]) == hex(0)

    vb.writePixel([399, 299], 9)
    assert vb.getPixel([399, 299]) == hex(0)

    vb.writePixel([0, 0], '0xFFFFFF')
    assert vb.getPixel([0, 0]) == '0xFFFFFF'
    
    vb.clearBuffer()
    assert vb.getPixel([0,0]) == hex(0)
