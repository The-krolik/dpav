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
            set_bit_number(int)
            set_sample_rate(int)
            set_audio_buffer()
            set_audio_device(int)

        Getters:
            get_bit_number()->int
            get_sample_rate()->int
            get_audio_buffer()
            get_audio_device()->Returns int corresponding to audio device

        Misc Variables:
            self.waves is the wave_table
            self.waveform is the current wave generator for sound
    """

    def __init__(
        self,
    ):  # TODO inheritance? if we inherited from a parent class, we could save what imports we would need here.
        """
        Constructor for the Audio class. Takes in TODO: Do we take in?
        """
        self._bit_number = 16
        self._sample_rate = 44100
        self._audio_buffer = numpy.zeros((self._sample_rate, 2), dtype=numpy.int32)
        # assumes a 1 second duration;
        # 32 bit int array handles 8, 16, or 32 for bit number;
        # support for other bit numbers pending
        # 2d for 2 channels
        self._audio_device = 0
        self.volume_level = 0.75
        self.waves = wave_table()

        self._audio_buffer = None
        self.waveform = self.waves.sin  # this is what the kids would call some bs
        self.name = 0

        self._audio_device = None

    """
    Locked to 16
    # bit number
    def set_bit_number(self, bit: int) -> None :
        #Sets the bit rate of the Audio class.
        #IN: Bit rate (Integer) <= 32
        #OUT: Returns None
        if(bit>=1 and bit<=32):
            self._bit_number = bit
        else:
            raise ValueError("Value must be a whole number greater than zero, less than or equal to 32")
    """

    def get_bit_number(self) -> int:
        """
        #Gets the bit rate of the Audio class.
        #IN: Nothing
        #OUT: Returns Bit rate as an integer
        """
        return self._bit_number

    """
    Locked to 44100
    # sample rate
    def set_sample_rate(self, sample: int) -> None:
        
        #Sets the sample rate of the Audio class.
        #IN: Sample rate (Integer). 44100 is default value
        #OUT: Returns None
        
        if(sample>0):
            self._sample_rate = sample
        else:
            raise ValueError("Sample rate has to be an integer greater than zero.")
    """

    def get_sample_rate(self) -> int:
        """
        #Gets the sample rate of the Audio class.
        #IN: None
        #OUT: Returns Sample rate (Integer). 44100 is default value
        """
        return self._sample_rate

    # audio buffer
    def set_audio_buffer(self, ab) -> None:
        """
        Sets the audio buffer of the Audio class
        IN: Requires a Numpy Array TODO: Type right?
        OUT: Return None
        """
        self._audio_buffer = ab

    def get_audio_buffer(self):  # TODO: need audio buffer type for return annotation
        """
        Returns the audio buffer of the Audio class
        IN: None
        OUT: Returns a Numpy Array TODO: Type right?
        """
        return self._audio_buffer

    # audio device
    def list_audio_devices(self) -> None:
        """
        Sets the current audio device of the Audio class.
        IN: Device Number (Integer).
        OUT: Returns None
        """
        pygame.mixer.init()
        print("Specify one of these devices' indices using set_audio_device")
        self._devices = sdl2.get_audio_device_names(False)
        for i, test in enumerate(self._devices):
            print(i, test)
        pygame.mixer.quit()

    def set_audio_device(self, device: int) -> int:
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
            self._audio_device = device
            # this is probably because of the environment not having audio devices.
            raise SystemError("No audio devices detected")

        if device > len(self._devices):
            raise ValueError("Device number exceeds known devices.")
        else:
            self._audio_device = device
        pygame.mixer.quit()

    def get_audio_device(self) -> int:
        """
        Gets the current audio device of the Audio class.
        IN: None
        OUT: Returns Device Number (Integer).
        """
        return self._audio_device

    def set_wave_form(self, wave) -> None:
        """
        Sets the expression governing the wave form playing. Uses this in buffer generation
        IN: takes a mathematical expression function 'pointer' in the form of f(inputfreq, timestep)
        OUT: none
        """
        self.waveform = wave
        pass

    def play_sound(self, input_frequency=0, input_duration=0) -> None:
        """
        Primary sound playing method of the audio class.
        IN: Takes an input frequency in Hz, and a duration in seconds
        OUT: Plays sound, nothing returned
        """
        if type(input_duration) is not int and type(input_duration) is not float:
            raise TypeError("The duration must be a number")
        elif input_duration < 0:
            raise ValueError("The duration must be non-negative")

        bit_number = self.get_bit_number()
        sample_rate = self.get_sample_rate()
        volume_level = self.volume_level
        number_samples = int(round(input_duration * sample_rate))
        max_sample = 2 ** (bit_number - 1) - 1

        # pygame.mixer.pre_init(sample_rate, -bit_number, 6)

        if (
            self._audio_device == None
        ):  # if the user hasn't specified an audio device they want to use, let pygame figure it out
            pygame.mixer.init(sample_rate, -bit_number, 2)
        else:  # otherwise, pull from the list of our devices using the index specified
            try:
                pygame.mixer.init(
                    sample_rate,
                    -bit_number,
                    2,
                    devicename=self._devices[self._audio_device],
                )
            except:
                pygame.mixer.init(sample_rate, -bit_number, 2)

        audio_buffer = (
            self.get_audio_buffer()
        )  # check if the user has specified their own audio buffer
        if isinstance(audio_buffer, type(None)):
            audio_buffer = numpy.zeros((number_samples, 2), dtype=numpy.int32)
            for s in range(number_samples):
                t = float(s) / sample_rate
                audio_buffer[s][0] = int(
                    round(volume_level * max_sample * self.waveform(input_frequency, t))
                )
                audio_buffer[s][1] = int(
                    round(volume_level * max_sample * self.waveform(input_frequency, t))
                )

        try:
            sound = pygame.sndarray.make_sound(audio_buffer)
            pygame.mixer.find_channel(force=False).play(sound)
        except AttributeError:
            print("Out of Channels")

    def wait_for_sound_end(self):
        """
        Function call that is placed at the end of scripts to keep processes going
        so that way sounds play to their full duration without a pygame window instance
        In: None
        Return: None
        """
        while pygame.mixer.get_busy():
            pass

    # pitch is semitones to transpose
    def playSample(self, sample_name: str) -> None:
        """
        Plays sounds that are wav, ogg or mp3 files.
        In: String path or name of sound
        Out: None
        """
        bit_number = self.get_bit_number()
        sample_rate = self.get_sample_rate()
        volume_level = self._volume_level

        if (
            self._audio_device == None
        ):  # if the user hasn't specified an audio device they want to use, let pygame figure it out
            pygame.mixer.init(sample_rate, -bit_number, 6)
        else:  # otherwise, pull from the list of our devices using the index specified
            try:
                pygame.mixer.init(
                    sample_rate,
                    -bit_number,
                    6,
                    devicename=self._devices[self._audio_device],
                )
            except:
                pygame.mixer.init(sample_rate, -bit_number, 6)

        sound = pygame.mixer.Sound(sample_name)
        pygame.mixer.Sound.play(sound)

    def __del__(self):
        pass


class wave_table:
    def __init__(self):
        pass

    def sin(self, input_frequency, t):
        return math.sin(2 * math.pi * input_frequency * t)

    def square(self, input_frequency, t):
        return round(math.sin(2 * math.pi * input_frequency * t))

    def noise(self, input_frequency, t):
        return random.random() * input_frequency * t

    def saw(self, input_frequency, t):
        return t * input_frequency - math.floor(t * input_frequency)

    def triangle(self, input_frequency, t):
        return 2 * abs(
            (t * input_frequency) / 1 - math.floor(((t * input_frequency) / 1) + 0.5)
        )
