import numpy, random

import pygame
from pygame.locals import *

import math
import numpy
from time import sleep

class Audio(object):
    """
    Handles Audio capabilities of Python Direct Platform.
    Here are the functions:
        Constructor:
            __init__()

        Setters:
            setBitNumber(int)
            setSampleRate(int)
            setAudioBuffer(TODO:TYPE)
            setAudioDevice(int)

        Getters:
            getBitNumber()->int
            getSampleRate()->int
            getAudioBuffer()->WHATEVER THIS IS
            getAudioDevice()->Returns int corresponding to audio device

        Misc Variables:
    """
    def __init__(self): #TODO inheritance? if we inherited from a parent class, we could save what imports we would need here.
        """
        Constructor for the Audio class. Takes in TODO: Do we take in?
        """
        self._bitNumber = 16
        self._sampleRate = 44100
        self._audioBuffer = numpy.zeros((self._sampleRate, 2), dtype = numpy.int32)
                                    #assumes a 1 second duration;
                                    #32 bit int array handles 8, 16, or 32 for bit number;
                                    #support for other bit numbers pending
                                    #2d for 2 channels
        self._audioDevice = 0
        self._volumeLevel = 0.75
        self.waves=waveTable()
    # bit number
    def setBitNumber(self, bit: int) -> None :
        """
        Sets the bit rate of the Audio class.
        IN: Bit rate (Integer) < 16
        OUT: Returns None
        """
        self._bitNumber = bit

    def getBitNumber(self) -> int :
        """
        Gets the bit rate of the Audio class.
        IN: Nothing
        OUT: Returns Bit rate as an integer
        """
        return self._bitNumber

    # sample rate
    def setSampleRate(self, sample: int) -> None:
        """
        Sets the sample rate of the Audio class.
        IN: Sample rate (Integer). 44100 is default value
        OUT: Returns None
        """
        self._sampleRate = sample

    def getSampleRate(self) -> int:
        """
        Gets the sample rate of the Audio class.
        IN: None
        OUT: Returns Sample rate (Integer). 44100 is default value
        """
        return self._sampleRate

    # audio buffer
    def setAudioBuffer(self, ab) -> None:
        """
        Sets the audio buffer of the Audio class
        IN: Requires a Numpy Array TODO: Type right?
        OUT: Return None
        """
        self._audioBuffer = ab

    def getAudioBuffer(self) : # TODO: need audio buffer type for return annotation
        """
        Returns the audio buffer of the Audio class
        IN: None
        OUT: Returns a Numpy Array TODO: Type right?
        """
        return self._audioBuffer

    # audio device
    def setAudioDevice(self, device: int) -> None:
        """
        Sets the current audio device of the Audio class.
        IN: Device Number (Integer).
        OUT: Returns None
        """
        self._audioDevice = device

    def getAudioDevice(self) -> int:
        """
        Gets the current audio device of the Audio class.
        IN: None
        OUT: Returns Device Number (Integer).
        """
        return self._audioDevice

    def playSound(self, inputFrequency, inputDuration)->None:
        """
        Primary sound playing method of the audio class.
        IN: Takes an input frequency in Hz, and a duration in seconds
        OUT: Plays sound, nothing returned
        """
        bitNumber = self.getBitNumber()
        sampleRate = self.getSampleRate()
        volumeLevel = self._volumeLevel
        numberSamples = int(round(inputDuration*sampleRate))
        audioBuffer = numpy.zeros((numberSamples, 2), dtype = numpy.int32)
        maxSample = 2**(bitNumber - 1) - 1

        pygame.mixer.pre_init(sampleRate, -bitNumber, 2)
        pygame.mixer.init()


        for s in range(numberSamples):
            t = float(s)/sampleRate
            audioBuffer[s][0] = int(round(volumeLevel*maxSample*self.waves.sin(inputFrequency,t)))
            audioBuffer[s][1] = int(round(volumeLevel*maxSample*self.waves.sin(inputFrequency,t)))

        sound = pygame.sndarray.make_sound(audioBuffer)
        pygame.mixer.find_channel().play(sound)
        #sound.play(loops = 0)
        #sleep(inputDuration)

class waveTable:
    def __init__(self):
        pass

    def sin(self, inputFrequency, t):
        return math.sin(2*math.pi*inputFrequency*t)

    def square(self, inputFrequency, t):
        return round(math.sin(2*math.pi*inputFrequency*t))

    def noise(self, inputFrequency, t):
        return random.random()*inputFrequency*t
