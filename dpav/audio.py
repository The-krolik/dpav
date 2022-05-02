import numpy, random
import pygame._sdl2 as sdl2

import pygame
from pygame.locals import *

import math
import numpy
from time import sleep


class Audio(object):
    """
    Handles Audio capabilities of Direct Python Audio/Video.
    
    Members:
        Private:
            _bit_number: An int for the bit rate (locked at 16).
            _sample_rate: An int for the sample rate (locked at 44100).
            _audio_buffer: A numpy array holding sounds to be played.
            _audio_device: An int for the array index of list of audio_devices (see set_audio_devices).

        Public:
            volume_level: A float between 0 and 1 for the volume.
            waves: A table of built in waveforms.
    """

    def __init__(self):
        """Constructor for the Audio class."""
        
        self._bit_number = 16
        self._sample_rate = 44100
        self._audio_buffer = numpy.zeros((self._sample_rate, 2), dtype=numpy.int32)
        # assumes a 1 second duration
        # 2d for 2 channels
        self._audio_device = 0
        self.volume_level = 0.75
        self.waves = wave_table()

        self._audio_buffer = None
        self.waveform = self.waves.sin
        self.name = 0

        self._audio_device = None

    def get_bit_number(self) -> int:
        """
        Gets the bit rate of the Audio class

        Returns:
            The bit rate of the Audio class.
    
        Notes:
            The bit rate is currently locked to 16 bits.
        """
        return self._bit_number

    def get_sample_rate(self) -> int:
        """
        Gets the sample rate of the Audio class.

        Returns:
            self._sample_rate: The sample rate of the audioClass - int value
            
        Notes:
            The sample rate is currently locked to 44100.
        """
        return self._sample_rate

    # audio buffer
    def set_audio_buffer(self, ab: np.ndarray) -> None:
        """
        Sets the audio buffer of the Audio Class.

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

        Args:
            ab: An array of shape(samples, channels) e.g. ab[44100][2]
        """
        self._audio_buffer = ab

    def get_audio_buffer(self) -> np.ndarray | none:
        """Returns the audio buffer of the Audio class."""
        return self._audio_buffer

    # audio device
    def list_audio_devices(self) -> None:
        """
        Lists the output devices on your system and adds to list self._devices.

        Run this function before using set_audio_device() to add devices to the list devices.

        Example:
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

    def set_audio_device(self, device: int) -> none:
        """
        Sets the current audio device of the Audio class.

        This can only be set ONCE per instance. To change devices, del the current instance
        set the new device, and continue
        This needs to be run after list_audio_device() in order to see list of audio devices
        If not run the device will default to the current device being used by the machine

        Args:
            device: The array index for the selected audio device.

        Example:
            audioobject.set_audio_device(2)
            Based on example in list_audio_devices() this would change the device to Speakers (HyperX Cloud II Wireless)
        """
        try:
            pygame.mixer.init()
            self._devices = sdl2.get_audio_device_names(False)
        except:
            self._audio_device = device
            # environment has no audio devices.
            raise SystemError("No audio devices detected")

        if device > len(self._devices):
            raise ValueError("Device number exceeds known devices.")
        else:
            self._audio_device = device
        pygame.mixer.quit()

    def get_audio_device(self) -> int:
        """Gets the current audio device number of the Audio Class."""
        return self._audio_device

    def set_waveform(self, wave) -> None:
        """
        Sets the waveform to be used for audio playback.

        play_audio uses this in buffer generation.



        Args:
            Wave: takes a mathematical expression function 'pointer' in the form of f(inputfreq, timestep).

        Example:
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

        - Play sounds directly from this function.
        - Need to run set_audio_device() or will default to the default audio device.
        - You can use set_waveform to change the type.
        - play_sound is somewhat overloaded to where if you have an audioBuffer set using set_audio_buffer, you can call play_sound().
            and it will play whatever that audio_buffer is e.g. wav files (Example in examples/custombuffer.py).
            play_sound(440, 1) would play an A note for one second with the sin waveform set.

        Args:
            input_frequency: Input frequency in Hz.
            input_duration: Duration in seconds.

        Raises:
            TypeError: If input_duration not a number, or < 0.
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
        ):  # if the user hasn't specified an audio device they want to use, pygame defaults
            pygame.mixer.init(sample_rate, -bit_number, 2)
        else:  # otherwise, pulls from the list of our devices using the index specified
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
        Function call that is placed at the end of scripts without a pygame window instance so sounds play to their full duration.

        Example:
            play_sound(440, 10)
            wait_for_sound_end() # This prevents the process from closing out before the sound ends.
        """
        while pygame.mixer.get_busy():
            pass

    # pitch is semitones to transpose
    def play_sample(self, sample_name: str) -> None:
        """
        Plays sounds that are wav, ogg or mp3 files.

        Args:
            sample_name: String path or name of sound

        Example:
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
    """This is a class holding waveforms for usage with the play_sound method.

    Example:
        waves = wave_table()
        sinefunc = waves.sin
    """

    def __init__(self):
        """Constructor for the wave_table class."""
        pass

    def sin(self, input_frequency: double, t: double) -> double:
        """
        Returns the value of a sine wave of a given frequency at a given time.

        This is the default waveform for the library.
        """
        return math.sin(2 * math.pi * input_frequency * t)

    def square(self, input_frequency: double, t: double) -> double:
        """Returns the value of a square wave of a given frequency at a given time."""
        return round(math.sin(2 * math.pi * input_frequency * t))

    def noise(self, input_frequency: double, t: double) -> double:
        """
        Random white noise.

        This waveform is quite loud.
        """
        return random.random() * input_frequency * t

    def saw(self, input_frequency: double, t: double) -> double:
        """Returns the value of a saw wave of a given frequency at a given time."""
        return t * input_frequency - math.floor(t * input_frequency)

    def triangle(self, input_frequency: double, t: double) -> double:
        """
        Returns the value of a triangle wave of a given frequency at a given time.

        This wave is similar in sound to a saw and sine wave together.
        """
        return 2 * abs(
            (t * input_frequency) / 1 - math.floor(((t * input_frequency) / 1) + 0.5)
        )
