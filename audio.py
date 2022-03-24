class Audio(object):
    def __init__(self): #TODO inheritance? if we inherited from a parent class, we could save what imports we would need here.
        self._bitNumber = 0
        self._sampleRate = 0
        self._audioBuffer = None # TODO: Figure out the type. numpy array of ints?
        self._audioDevice = 0
        self._volumeLevel = 0.0

    # bit number    
    def setBitNumber(self, bit: int) -> None :
        self._bitNumber = bit
        
    def getBitNumber(self) -> int :
        return self._bitNumber

    # sample rate
    def setSampleRate(self, sample: int) -> None:
        self._sampleRate = sample

    def getSampleRate(self) -> int:
        return self._sampleRate

    # audio buffer
    def setAudioBuffer(self, ab) -> None:
        self._audioBuffer = ab

    def getAudioBuffer(self) : # TODO: need audio buffer type for return annotation
        return self._audioBuffer

    # audio device
    def setAudioDevice(self, device: int) -> None:
        self._audioDevice = device

    def getAudioDevice(self) -> int:
        return self._audioDevice

test = Audio()

test.setBitNumber(24)
gettest=test.getBitNumber()
print("bit rate ok",gettest)

auBuf=[1,2,3,4]
test.setAudioBuffer(auBuf)
gettest=test.getAudioBuffer()
print("audio buff ok",gettest)

test.setSampleRate(24)
gettest=test.getSampleRate()
print("samp rate ok", gettest)

test.setAudioDevice(1)
gettest=test.getAudioDevice()
print("audio device ok", gettest)




