from datetime import datetime
from vbuffer import VBuffer
import numpy as np
import pygame


def _debugOut(msg):

    date_time = datetime.now()
    date = date_time.strftime("%Y%m%d")
    time = date_time.strftime("%H:%M:%S")

    msg = "{} | {}\n".format(time, msg) 
    filename = "./logs/{}.txt".format(date)
    with open(filename, 'a') as file:
        file.write(msg)

def drawRect(vbuffer, color, pt1, pt2):
    
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
        
'''
Description:
    Takes the file path of an image and returns an np.ndarray in hex
'''
def loadImage(filepath) -> np.ndarray:
    imagesurf = pygame.image.load(filepath)
    image_array = pygame.surfarray.array3d(imagesurf)
    return rgb2hex(image_array)

'''
Description:
    Takes an np.ndarray in rgb and returns it in hex
'''
def rgb2hex(arr):
    ret = np.zeros((arr.shape[0],arr.shape[1]))
    
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            red = arr[i,j,0] << 16
            green = arr[i,j,1] << 8
            blue = arr[i,j,2]
            ret[i,j] = red + green + blue
                       
                       
    return ret