import audio
import pygame, pygame.midi

test = audio.Audio()
pygame.init()
pygame.midi.init()
for x in range(0, pygame.midi.get_count()):
    print(pygame.midi.get_device_info(x)[1], pygame.midi.get_device_info(x)[2])
test.setWaveForm(test.waves.sin)
inp = pygame.midi.Input(1)
_running = True
while _running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _running = False
            break
    if inp.poll():
        data = inp.read(1000)[0][0]
        print(data, data[1])

        # 60 is midi middle C
        # If we want HZ of note, we take notedistance=midiread-60
        # then do 261.625565 * 2 ** (notedistance/12)
        # see this for tunings: http://techlib.com/reference/musical_note_frequencies.htm#:~:text=Starting%20at%20any%20note%20the,away%20from%20the%20starting%20note.
        if data[0] != 128:
            noteDistance = data[1] - 60
            hz = 261.625565 * 2 ** (noteDistance / 12)
            test.playSound(hz, 0.5)
pygame.quit()
