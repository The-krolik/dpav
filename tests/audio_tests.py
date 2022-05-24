import pytest
import dpav as dp

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
