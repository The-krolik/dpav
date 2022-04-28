import math
import dypi


class Key:
    def __init__(self, loc, keytype, note, octave):
        self.loc = loc
        self.type = keytype
        self.note = note
        self.octave = octave


def playKey(pos, wsize, bKeys, wKeys):

    x, y = pos[0], pos[1]
    bInd = min(math.floor(x / wsize * 5 / 7), len(bKeys) - 1)
    wInd = math.floor(x / wsize)
    bKey = bKeys[bInd]
    wKey = wKeys[wInd]

    key = wKey
    if (
        x >= bKey.loc[0][0]
        and x <= bKey.loc[1][0]
        and y >= bKey.loc[0][1]
        and y <= bKey.loc[1][1]
    ):
        key = bKey

    frequency = math.ceil(dypi.get_note_from_string(key.note, key.octave))
    mySound = dypi.Audio()
    mySound.play_sound(frequency, 0.25)


def drawWhiteKeys(buf, numKeys, keySize, keySpacing):

    x = 0
    wKeys = []
    dim = buf.get_dimensions()

    drawkey = True
    for i in range(numKeys * 2 - 1):
        if drawkey:
            start = (x, 0)
            end = (x + keySize, dim[1])
            dypi.draw_rectangle(buf, 0xFFFFFF, start, end)
            wKeys.append(Key([start, end], "white", None, None))
            x += keySize
        else:
            start = (x, 0)
            end = (x + keySpacing, dim[1])
            dypi.draw_rectangle(buf, 0x000000, start, end)
            x += keySpacing

        drawkey = True if drawkey == False else False

    return wKeys


def drawBlackKeys(buf, numWKeys, wkeySize, wkeySpacing):

    drawkey = True
    bkeySize = round(wkeySize * 2 / 3)
    if bkeySize % 2 == 0:
        bkeySize += 1

    dim = buf.get_dimensions()
    bKeys = []
    x = wkeySize - round(bkeySize / 2)
    for i in range(1, round(numWKeys * 5 / 7)):
        start = (x, 0)
        end = (x + bkeySize, round(dim[1] * 2 / 3))
        dypi.draw_rectangle(buf, 0x000000, start, end)
        bKeys.append(Key([start, end], "black", None, None))

        x += wkeySize + wkeySpacing
        if i % 5 in [0, 2]:
            x += wkeySize + wkeySpacing

    return bKeys


def getKeyNoteDict():
    white = {
        "1": "C",
        "2": "D",
        "3": "E",
        "4": "F",
        "5": "G",
        "6": "A",
        "7": "B",
        "8": "C",
        "9": "D",
        "0": "E",
        "-": "F",
        "=": "G",
        "q": "A",
        "w": "B",
        "e": "C",
        "r": "D",
        "t": "E",
        "y": "F",
        "u": "G",
        "i": "A",
        "o": "B",
        "p": "C",
    }
    black = {
        "a": "C#",
        "s": "D#",
        "d": "F#",
        "f": "G#",
        "g": "A#",
        "h": "C#",
        "j": "D#",
        "k": "F#",
        "l": "G#",
        "z": "A#",
        "x": "C#",
        "c": "D#",
        "v": "F#",
        "b": "G#",
        "n": "A#",
    }

    return white, black


if __name__ == "__main__":

    wevents, bevents = getKeyNoteDict()

    num_wkeys = 22
    wkey_size = 35
    wkey_spacing = 3

    windowx = (wkey_size * num_wkeys) + ((num_wkeys - 1) * wkey_spacing)
    buf = dypi.VBuffer((windowx, 300))
    wKeys = drawWhiteKeys(buf, num_wkeys, wkey_size, wkey_spacing)
    bKeys = drawBlackKeys(buf, num_wkeys, wkey_size, wkey_spacing)

    for ind, v in enumerate(wevents.values()):
        wKeys[ind].note = v
    for ind, v in enumerate(bevents.values()):
        bKeys[ind].note = v
    for ind, v in enumerate(bevents.values()):
        wKeys[ind].octave = math.ceil((ind + 3) / 7 + 2)
    for ind, v in enumerate(bevents.values()):
        bKeys[ind].octave = math.ceil((ind + 2) / 5 + 2)

    window = dypi.Window(buf)
    window.open()
    mySound = dypi.Audio()

    while window.is_open():
        for i, event in enumerate(wevents):
            if event in window.eventq:
                key = wKeys[i]
                frequency = math.ceil(dypi.get_note_from_string(key.note, key.octave))
                mySound.play_sound(frequency, 0.25)

        for i, event in enumerate(bevents):
            if event in window.eventq:
                key = wKeys[i]
                frequency = math.ceil(dypi.get_note_from_string(key.note, key.octave))
                mySound.play_sound(frequency, 0.25)

        if "mouse" in window.eventq:
            pos = window.get_mouse_pos()
            playKey(pos, wkey_size + wkey_spacing, bKeys, wKeys)
