from datetime import datetime
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