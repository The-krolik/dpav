def getNote(string, octave):
    notes = {'A':-3,'B':-1,'C':0,'D':2,'E':4, 'F':5,'G':7}
    tone=None
    if len(string)>0:
        if string[0].upper() in notes:
            tone=notes[string[0]]
        for each in string:
            if each =='b': tone-=1
            elif each=='#': tone+=1
        # 60 is midi middle C
        # If we want HZ of note, we take notedistance=midiread-60
        # then do 261.625565 * 2 ** (notedistance/12)
        # see this for tunings: http://techlib.com/reference/musical_note_frequencies.htm#:~:text=Starting%20at%20any%20note%20the,away%20from%20the%20starting%20note.
        # C4 is middle C

    #tone needs to be distance from C
    octavedisc=octave-3
    tone = octavedisc*12 + tone
    hz = 261.625565 * 2 ** (tone/12)

    print(hz)
getNote('C',4)
