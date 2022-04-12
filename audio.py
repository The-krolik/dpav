import numpy, random
import pygame._sdl2 as sdl2

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
            setAudioBuffer()
            setAudioDevice(int)

        Getters:
            getBitNumber()->int
            getSampleRate()->int
            getAudioBuffer()
            getAudioDevice()->Returns int corresponding to audio device

        Misc Variables:
            self.waves is the wavetable
            self.waveform is the current wave generator for sound
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
        self.volumeLevel = 0.75
        self.waves=waveTable()
        self.waveform = self.waves.sin # this is what the kids would call some bs
        self.name=0

        self._audioDevice=None
        
    """
    Locked to 16
    # bit number
    def setBitNumber(self, bit: int) -> None :
        #Sets the bit rate of the Audio class.
        #IN: Bit rate (Integer) <= 32
        #OUT: Returns None
        if(bit>=1 and bit<=32):
            self._bitNumber = bit
        else:
            raise ValueError("Value must be a whole number greater than zero, less than or equal to 32")
    """

    def getBitNumber(self) -> int :
        """
        #Gets the bit rate of the Audio class.
        #IN: Nothing
        #OUT: Returns Bit rate as an integer
        """
        return self._bitNumber
    
    """
    Locked to 44100
    # sample rate
    def setSampleRate(self, sample: int) -> None:
        
        #Sets the sample rate of the Audio class.
        #IN: Sample rate (Integer). 44100 is default value
        #OUT: Returns None
        
        if(sample>0):
            self._sampleRate = sample
        else:
            raise ValueError("Sample rate has to be an integer greater than zero.")
    """
    def getSampleRate(self) -> int:
        """
        #Gets the sample rate of the Audio class.
        #IN: None
        #OUT: Returns Sample rate (Integer). 44100 is default value
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
    def listAudioDevices(self) -> None:
        """
        Sets the current audio device of the Audio class.
        IN: Device Number (Integer).
        OUT: Returns None
        """
        pygame.mixer.init()
        print("Specify one of these devices' indices using setAudioDevice")
        self._devices = sdl2.get_audio_device_names(False)
        for i,test in enumerate(self._devices):
            print(i,test)
        pygame.mixer.quit()

    def setAudioDevice(self, device: int) -> int:
        """
        Sets the current audio device of the Audio class. 
        NOTE: This can only be set ONCE per instance. To change devices, del the current instance
        set the new device, and continue
        IN: Audio device corresponding to array index of audio devices
        OUT: None
        """
        try:
            pygame.mixer.init()
            self._devices = sdl2.get_audio_device_names(False)
        except:
            self._audioDevice = device
            # this is probably because of the environment not having audio devices.
            raise SystemError("No audio devices detected")

        if(device>len(self._devices)):
            raise ValueError("Device number exceeds known devices.")
        else:
            self._audioDevice = device
        pygame.mixer.quit()

    def getAudioDevice(self) -> int:
        """
        Gets the current audio device of the Audio class.
        IN: None
        OUT: Returns Device Number (Integer).
        """
        return self._audioDevice

    def setWaveForm(self, wave)->None:
        """
        Sets the expression governing the wave form playing. Uses this in buffer generation
        IN: takes a mathematical expression function 'pointer' in the form of f(inputfreq, timestep)
        OUT: none
        """
        self.waveform = wave
        pass

    def playSound(self, inputFrequency, inputDuration)->None:
        """
        Primary sound playing method of the audio class.
        IN: Takes an input frequency in Hz, and a duration in seconds
        OUT: Plays sound, nothing returned
        """
        if type(inputDuration) is not int and type(inputDuration) is not float:
            raise TypeError("The duration must be a number")
        elif inputDuration < 0:
            raise ValueError("The duration must be non-negative")
        
        bitNumber = self.getBitNumber()
        sampleRate = self.getSampleRate()
        volumeLevel = self.volumeLevel
        numberSamples = int(round(inputDuration*sampleRate))
        audioBuffer = numpy.zeros((numberSamples, 2), dtype = numpy.int32)
        maxSample = 2**(bitNumber - 1) - 1

        #pygame.mixer.pre_init(sampleRate, -bitNumber, 6)

        if(self._audioDevice==None): # if the user hasn't specified an audio device they want to use, let pygame figure it out
            pygame.mixer.init(sampleRate, -bitNumber, 6)
        else: # otherwise, pull from the list of our devices using the index specified
            try:
                pygame.mixer.init(sampleRate,-bitNumber,6, devicename=self._devices[self._audioDevice])
            except:
                pygame.mixer.init(sampleRate, -bitNumber, 6)

        for s in range(numberSamples):
            t = float(s)/sampleRate
            audioBuffer[s][0] = int(round(volumeLevel*maxSample*self.waveform(inputFrequency,t)))
            audioBuffer[s][1] = int(round(volumeLevel*maxSample*self.waveform(inputFrequency,t)))
        try:
            sound = pygame.sndarray.make_sound(audioBuffer)
            pygame.mixer.find_channel(force=False).play(sound)
        except AttributeError:
            print("Out of Channels")

    def waitForSoundEnd(self):
        """
        Function call that is placed at the end of scripts to keep processes going
        so that way sounds play to their full duration without a pygame window instance
        In: None
        Return: None
        """
        while(pygame.mixer.get_busy()):
            pass

    # pitch is semitones to transpose
    def playSample(self, sampleName: str)->None:
        """
        Plays sounds that are wav, ogg or mp3 files.
        In: String path or name of sound
        Out: None
        """
        bitNumber = self.getBitNumber()
        sampleRate = self.getSampleRate()
        volumeLevel = self._volumeLevel

        if(self._audioDevice==None): # if the user hasn't specified an audio device they want to use, let pygame figure it out
            pygame.mixer.init(sampleRate, -bitNumber, 6)
        else: # otherwise, pull from the list of our devices using the index specified
            try:
                pygame.mixer.init(sampleRate,-bitNumber,6, devicename=self._devices[self._audioDevice])
            except:
                pygame.mixer.init(sampleRate, -bitNumber, 6)

        sound = pygame.mixer.Sound(sampleName)
        pygame.mixer.Sound.play(sound)


    def __del__(self):
        pass

class waveTable:
    def __init__(self):
        pass

    def sin(self, inputFrequency, t):
        return math.sin(2*math.pi*inputFrequency*t)

    def square(self, inputFrequency, t):
        return round(math.sin(2*math.pi*inputFrequency*t))

    def noise(self, inputFrequency, t):
        return random.random()*inputFrequency*t

    def saw(self, inputFrequency, t):
        return (t*inputFrequency-math.floor(t*inputFrequency))

    def triangle(self,inputFrequency, t):
        return 2*abs( (t*inputFrequency)/1 - math.floor( ((t*inputFrequency)/1)+0.5 ))
