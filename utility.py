from datetime import datetime

def getNoteFromString(string, octave):
    """
    Given a string representing a note, this will return a hz
    IN: string representing the note e.g. Ab, C, E#
    OUT: returns hz
    """
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
    octavedisc=octave-4
    tone = octavedisc*12 + tone
    hz = 261.625565 * 2 ** (tone/12)
    return hz
def _debugOut(msg):

    date_time = datetime.now()
    date = date_time.strftime("%Y%m%d")
    time = date_time.strftime("%H:%M:%S")

    msg = "{} | {}\n".format(time, msg) 
    filename = "./logs/{}.txt".format(date)
    with open(filename, 'a') as file:
        file.write(msg)
