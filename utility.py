from datetime import datetime
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

        
def load_image(filepath) -> np.ndarray:
    """
    Description:
        Takes the file path of an image and returns an np.ndarray in hex
    """
    imagesurf = pygame.image.load(filepath)
    image_array = pygame.surfarray.array3d(imagesurf)
    return rgb2hex(image_array)


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
