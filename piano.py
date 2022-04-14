import os
import sys
import numpy as np
import math

from window import Window
from vbuffer import VBuffer
from audio import Audio
import utility as util

class Key:
    def __init__(self, loc, keytype, note, octave):
        self.loc = loc
        self.type = keytype
        self.note = note  
        self.octave = octave
        
        
def playKey(pos, wsize, bKeys, wKeys):
    
    x,y = pos[0],pos[1]
    bInd = math.floor(x/wsize * 5/7)
    wInd = math.floor(x/wsize)
    bKey = bKeys[bInd]
    wKey = wKeys[wInd]
    
    key = wKey
    if x >= bKey.loc[0][0] and x <= bKey.loc[1][0] and y >= bKey.loc[0][1] and y <= bKey.loc[1][1]:
        key = bKey
        
    #PLAY NOTE stored in key variable
    frequency = util.getNoteFromString(key.note, key.octave)
    print(frequency)
    mySound = Audio()
    mySound.playSound(frequency, .5)
    

def drawWhiteKeys(buf, numKeys, keySize, keySpacing):
    drawkey = True
    x = 0
    wKeys = []
    dim = buf.getDimensions()
    for i in range(numKeys*2 - 1):
        if drawkey:
            start = (x,0)
            end = (x+keySize,dim[1])
            util.draw_rect(buf,0xffffff,start,end)
            wKeys.append(Key([start,end],"white",None,None))
            x += keySize
        else:
            start = (x,0)
            end = (x+keySpacing,dim[1])
            util.draw_rect(buf,0x000000,start,end)
            x += keySpacing

        drawkey = True if drawkey == False else False
        
    return wKeys
        
def drawBlackKeys(buf, numWKeys, wkeySize, wkeySpacing):
    
    drawkey = True
    bkeySize = round(wkeySize * 2 /3)
    if (bkeySize % 2==0): bkeySize += 1
    
    dim = buf.getDimensions()
    bKeys = []
    x = wkeySize - round(bkeySize/2)
    for i in range(1,round(numWKeys*5/7)):
        start = (x,0)
        end = (x+bkeySize,round(dim[1] * 2/3))
        util.draw_rect(buf,0x000000,start,end)
        bKeys.append(Key([start,end],"black",None,None))

        x += wkeySize + wkeySpacing
        if (i % 5 in [0,2]):
            x += wkeySize + wkeySpacing
            
    return bKeys
            

def getWhiteNotes():
    return ['C', 'D', 'E', 'F', 'G', 'A', 'B', 
            'C', 'D', 'E', 'F', 'G', 'A', 'B', 
            'C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']

def getBlackNotes():
    return ['C#', 'D#', 'F#', 'G#', 'A#', 
            'C#', 'D#', 'F#', 'G#', 'A#', 
            'C#', 'D#', 'F#', 'G#', 'A#']

white_keys = 22
wkey_size = 35
wkey_spacing = 3

xdim = (wkey_size * white_keys) + ((white_keys - 1) * wkey_spacing)
buf = VBuffer((xdim,300))

wKeys = drawWhiteKeys(buf,white_keys,wkey_size,wkey_spacing)
bKeys = drawBlackKeys(buf,white_keys,wkey_size,wkey_spacing)

wNotes = getWhiteNotes()  
bNotes = getBlackNotes()  
for i in range(len(wNotes)):
     wKeys[i].note = wNotes[i]
for i in range(len(bNotes)):
     bKeys[i].note = bNotes[i]
for i in range(len(wNotes)):
     wKeys[i].octave = math.ceil(i/7+2)
for i in range(len(bNotes)):
     bKeys[i].octave = math.ceil(i/5+2)



window = Window(buf)
window.open()
while window.isOpen:
    
    if 'mouse' in window.activeEvents:
        pos = window.getMousePosition()
        playKey(pos,wkey_size+wkey_spacing,bKeys,wKeys)
    
    window.update()