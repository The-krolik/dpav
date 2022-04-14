from datetime import datetime
from vbuffer import VBuffer
import numpy as np
import pygame


def _debug_out(msg):
    date_time = datetime.now()
    date = date_time.strftime("%Y%m%d")
    time = date_time.strftime("%H:%M:%S")

    msg = "{} | {}\n".format(time, msg) 
    filename = "./logs/{}.txt".format(date)
    with open(filename, 'a') as file:
        file.write(msg)

def draw_rect(vbuffer, color, pt1, pt2):
    
    pts = [pt1,pt2]
    
    # error checking
    if type(vbuffer) != VBuffer and type(vbuffer) != np.ndarray:
        raise TypeError("arg1 must be of type vbuffer or numpy.ndarray")
        
    if type(color) != int or color < 0 or color > 16777215:
        raise ValueError("arg2 must be of type integer in range 0-16777215")
    
    for pt in pts:
        if (((type(pt) != tuple) and (type(pt) != list)) or (len(pt) > 2) or (len(pt) < 2)):
            raise TypeError("arg3 & arg4 must be a tuple or list of 2 int elements")
        for val in pt:
            if type(val) != int:
                raise TypeError("arg3 & arg4 must be a tuple or list of 2 int elements")
                
    
    if type(vbuffer) == VBuffer:
        buf = vbuffer.buffer
    elif type(vbuffer) == np.ndarray:
        buf = vbuffer
    
    
    lowx,highx = min(pt1[0],pt2[0]), max(pt1[0],pt2[0])
    lowy,highy = min(pt1[1],pt2[1]), max(pt1[1],pt2[1])
    
    buf[lowx:highx, lowy:highy] = color
        
def load_image(filepath) -> np.ndarray:
    """
    Description:
        Takes the file path of an image and returns an np.ndarray in hex
    """
    imagesurf = pygame.image.load(filepath)
    image_array = pygame.surfarray.array3d(imagesurf)
    return rgb_to_hex(image_array)


def rgb_to_hex(arr):
    """
    Description:
        Takes an np.ndarray in rgb and returns it in hex
    """
    ret = np.zeros((arr.shape[0],arr.shape[1]))
    
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            red = arr[i,j,0] << 16
            green = arr[i,j,1] << 8
            blue = arr[i,j,2]
            ret[i,j] = red + green + blue
                       
    return ret


def draw_circle(buf, center, r, color):
    """
    Description:
        Draws a circle at a given center of radius r on a visual buffer buf
        colored color
    """
    center_x = center[0]
    center_y = center[1]
    x = r
    y = 0

    buf[x+center_x][y+center_y] = color
    if r > 0:
        buf[x+center_x][-y+center_y] = color
        buf[y+center_x][x+center_y] = color
        buf[-y+center_x][x+center_y] = color

    P = 1 - r
    while x > y:
        y += 1
        if P <= 0:
            P = P + 2*y + 1
        else:
            x -= 1
            P = P + 2*y - 2*x + 1

        if x < y:
            break

        buf[x+center_x][y+center_y] = color
        buf[-x+center_x][y+center_y] = color
        buf[x+center_x][-y+center_y] = color
        buf[-x+center_x][-y+center_y] = color
        
        if x != y:
            buf[y+center_x][x+center_y] = color
            buf[-y+center_x][x+center_y] = color
            buf[y+center_x][-x+center_y] = color
            buf[-y+center_x][-x+center_y] = color


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