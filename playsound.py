import pygame
from pygame.locals import *

import math
import numpy
from time import sleep

def playSound(inputFrequency, inputDuration):
    bitNumber = 16
    sampleRate = 44100
    volumeLevel = 0.75
    numberSamples = int(round(inputDuration*sampleRate))
    audioBuffer = numpy.zeros((numberSamples, 2), dtype = numpy.int32)
    maxSample = 2**(bitNumber - 1) - 1
    
    pygame.mixer.pre_init(sampleRate, -bitNumber, 2)
    pygame.mixer.init()
    
    
    for s in range(numberSamples):
        t = float(s)/sampleRate
        audioBuffer[s][0] = int(round(volumeLevel*maxSample*math.sin(2*math.pi*inputFrequency*t)))
        audioBuffer[s][1] = int(round(volumeLevel*maxSample*math.sin(2*math.pi*inputFrequency*t)))
    
    sound = pygame.sndarray.make_sound(audioBuffer)
    sound.play(loops = 0)
    sleep(inputDuration)
    
playSound(262, 5)