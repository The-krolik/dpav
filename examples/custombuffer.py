import directpythonplatform as dpp
from directpythonplatform import Audio
import time,math
import numpy
import utility
test=dpp.Audio()
#test.listAudioDevices()
#test.setAudioDevice(4)
# the above are commented out so that way audio goes to your default device, but they can be handy in diagnosing issues
# or customizing your setup

# It is important that your bitNumber you set here is the same as whatever data you are trying to read in
#, or else you have a massive amount of static. 
# The point of this is to show that you can generate your own data and pass it to the interface

WAVEXAMPLE=True # change this if you want to hear the sin example
test._bitNumber=16 
if(WAVEXAMPLE!=True):
    # 44100 = sample rate
    # 32767 is 2 ^ (our bit depth -1)-1 and is essentially the number of samples per time stamp
    # 260 and 290 are our tones in hz
    # Below generates a buffer 1 second long of sin wave data-identical to the method used in house
    data = numpy.zeros((44100, 2), dtype = numpy.int16)
    for s in range(44100):
        t = float(s)/44100
        data[s][0] = int(round(32767*math.sin(2*math.pi*260*t)))
        data[s][1] = int(round(32767*math.sin(2*math.pi*290*t)))
else:
    # the library will attempt to read the wave file
    # this utility function WILL NOT work with 24bit int wavs, or 32bit float wavs as of 4/13/2022
    # it will work with 16 bit wavs
    ehh, data = utility.sixteenWavtoRawData('dpp.wav')
    print(data.shape, data.dtype) # we fetched a wav file's raw data, put it into a numpy array

test.setAudioBuffer(data) # either one of our numpy arrays are sent to audio.py for the playSound method

test.playSound()# notice playSound does not have any arguments. It's kind of implied that if you
                # set your audio buffer to something custom, you don't supply any.

test.waitForSoundEnd() # this makes the audio call blocking to prevent any premature stops
