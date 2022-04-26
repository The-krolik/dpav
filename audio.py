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

        Functions:
            play_sound(Hz, length)
                If audio buffer is set:
                    play_sound()
            play_sample(string_name_of_wav_file)

        Setters:
            set_audio_buffer(numpyarray)
            set_audio_device(int)
            set_waveform(waveform)
        Getters:
            get_bit_number()->int
            get_sample_rate()->int
            get_audio_buffer()
            get_audio_device()->Returns int corresponding to audio device
        Misc:
            list_audio_devices()
            wait_for_sound_end()
    """

    def __init__(
        self,
    ):
        """
        Constructor for the Audio class.
        Parameters:
            None
        Members:
            Private:
                _bit_number         int (locked)    --Bit rate of audio
                _sample_rate        int (locked)    --Sample rate of audio
                _audio_buffer       numpy array     --Audio buffer array of data
                self._audio_device  int             --Array index of list of audio_devices (see set_audio_devices)
                                                        where playback will occur


            Public:
                self.volume_level   float (<=1)     --Volume level for playback
                self.waves          wave_table      --Built in wave forms: sin, square, saw, noise, triangle

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

    def get_bit_number(self) -> int:
        """
        Gets the bit rate of the Audio class
        Parameters:
            None
        Returns:
            self._bit_number: The bit rate of the Audio class - int value
        Notes:
            Bit rate currently locked to 16 bits
        Examples:
            audioobject.get_bit_number(): returns the bit rate of the audio class
        """
        return self._bit_number
   def get_sample_rate(self) -> int:
        """
        Gets the sample rate of the Audio class.
        Parameters:
            None
        Returns:
            self._sample_rate: The sample rate of the audioClass - int value
        Notes:
            Sample rate is currently locked to 44100
        Examples:
            audioobject.get_sample_rate(): Gets the sample rate of the Audio class
        """
        return self._sample_rate

    # audio buffer
    def set_audio_buffer(self, ab) -> None:
        """
        Sets the audio buffer of the Audio Class.
        Parameters:
            ab: numpy array of shape(samples, channels) e.g. ab[44100][2]
        Returns:
            None
        Notes:
            The audio buffer needs to have two rows so that way stereo works as intended.
            You can set the audio buffer to wav file data by fetching numpy arrays using wav or scipy,
            however only 16 bit waves are supported. This process can be seen in custom_buffer.py w/ the
            utility function sixteenWavtoRawData

        Examples:
            # 44100 = sample rate
            # 32767 is 2 ^ (our bit depth -1)-1 and is essentially the number of samples per time stamp
            # 260 and 290 are our tones in hz
            # Below generates a buffer 1 second long of sin wave data-identical to the method used in house
            data = numpy.zeros((44100, 2), dtype=numpy.int16)
            for s in range(44100):
                t = float(s) / 44100
                data[s][0] = int(round(32767 * math.sin(2 * math.pi * 260 * t)))
                data[s][1] = int(round(32767 * math.sin(2 * math.pi * 290 * t)))
            audioobject.set_audio_buffer(data)

        """
        self._audio_buffer = ab

    def get_audio_buffer(self):  # TODO: need audio buffer type for return annotation
        """
        Returns the audio buffer of the Audio class
        Parameters:
            None
        Returns:
            self._audio_buffer: numpy array
        Notes:
            This will return none if the audio buffer has not been set by the set_audio_buffer method.
        Examples:
            audioobject.get_audio_buffer()

        """
        return self._audio_buffer

    # audio device
    def list_audio_devices(self) -> None:
        """
        Lists the output devices on your device and adds to list self._devices
        Parameters:
            None
        Returns:
            None
        Notes:
            Run this function before using set_audio_device() to add devices to the list devices
        Examples:
            audioobject.list_audio_devices()
            0 Speakers (Realtek(R) Audio)
            1 VGA248 (2-NVIDIA High Def Audio)
            2 Speakers (HyperX Cloud II Wireless)

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
        Parameters:
            device: int value - see all int values for each device by running list_audio_devices()
        Returns:
            None
        Notes:
            This can only be set ONCE per instance. To change devices, del the current instance
            set the new device, and continue
            This needs to be run after list_audio_device() in order to see list of audio devices
            If not run the device will default to the current device being used by the machine
        Examples:
            audioobject.set_audio_device(2)
            Based on example in list_audio_devices() this would change the device to Speakers (HyperX Cloud II Wireless)
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
        Gets the current audio device number of the Audio Class
        Parameters:
            None
        Returns
            self._audio_device: int value
        Notes:
            Returns the integer value of the device not the device name
        Examples:
            audioobject.get_audio_device() would return 2 based on example in set_audio_device(2)
        """
        return self._audio_device

    def set_waveform(self, wave) -> None:
        """
        Sets the expression governing the wave form playing
        Parameters:
            Wave: takes a mathematical expression function 'pointer' in the form of f(inputfreq, timestep)
        Returns:
            None
        Notes:
            Uses this in buffer generation
        Examples:
            audioobject.set_waveform(object.wave_table.sin)
            This would change to the waveform sin contained in the wave_table class
            The wave functions need to take in a input frequency as well as a timestep parameter
            to solve for a particular frequency at a given time step. See wave_table for an example of this.
        """
        self.waveform = wave
        pass

    def play_sound(self, input_frequency=0, input_duration=0) -> None:
        """
        Primary sound playing method of the audio class.
        Parameters:
            input_frequency: int value - input frequency in Hz
            input_duration: int value - duration in seconds
        Returns:
            None
        Notes:
            Plays the sound directly from this function
            Need to run set_audio_device() or will default to the default audio device
            You can use set_waveform to change the type.
            play_sound is somewhat overloaded to where if you have an audioBuffer set using set_audio_buffer, you can call play_sound()
                                                                            and it will play whatever that audio_buffer is e.g. wav files
                                                                            Example in examples/custombuffer.py
        Examples:
            play_sound(440, 1) would play an A note for one second with the sin waveform set.

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
        Parameters:
            None
        Returns:
            None
        Notes:

        Examples:
            play_sound(440, 10)
            wait_for_sound_end() # This prevents the process from closing out before the sound ends.
        """
        while pygame.mixer.get_busy():
            pass

    # pitch is semitones to transpose
    def play_sample(self, sample_name: str) -> None:
        """
        Plays sounds that are wav, ogg or mp3 files.
        Parameters:
            sample_name: String path or name of sound
        Returns:
            None
        Notes:

        Examples:
            audioobject.play_sample(mypath.mp3) would play sounds from the file mypath.mp3
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
        """
        Constructor for the wave_table class
        Parameters:
            None
        Returns:
            None
        Notes:

        Examples:

        """
        pass

    def sin(self, input_frequency, t):
        """

        Parameters:
            input_frequency:
            t:
        Returns:
            math.sin(2 * math.pi * input_frequency * t):
        Notes:

        Examples:

        """
        return math.sin(2 * math.pi * input_frequency * t)

    def square(self, input_frequency, t):
        """

        Parameters:
            input_frequency:
            t:
        Returns:
            round(math.sin(2 * math.pi * input_frequency * t)):
        Notes:

        Examples:

        """
        return round(math.sin(2 * math.pi * input_frequency * t))

    def noise(self, input_frequency, t):
        """

        Parameters:
            input_frequency:
            t:
        Returns:
            random.random() * input_frequency * t:
        Notes:
            VERY LOUD...be careful.
        Examples:

        """
        return random.random() * input_frequency * t

    def saw(self, input_frequency, t):
        """

        Parameters:
            input_frequency:
            t:
        Returns:
            t * input_frequency - math.floor(t * input_frequency):
        Notes:

        Examples:

        """
        return t * input_frequency - math.floor(t * input_frequency)

    def triangle(self, input_frequency, t):
        """

        Parameters:
            input_frequency:
            t:
        Returns:
            2 * abs((t * input_frequency) / 1 - math.floor(((t * input_frequency) / 1) + 0.5)):
        Notes:

        Examples:

        """
        return 2 * abs(
            (t * input_frequency) / 1 - math.floor(((t * input_frequency) / 1) + 0.5)
        )
