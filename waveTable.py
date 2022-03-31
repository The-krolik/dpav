import math, random
class waveTable:
    def __init__(self):
        pass

    def sin(self, inputFrequency, t):
        return math.sin(2*math.pi*inputFrequency*t)

    def square(self, inputFrequency, t):
        return round(math.sin(2*math.pi*inputFrequency*t))

    def noise(self, inputFrequency, t):
        return random.random()*inputFrequency*t
