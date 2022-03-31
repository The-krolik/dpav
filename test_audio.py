import audio as aud

def test_audio():
    a = aud.Audio()


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
