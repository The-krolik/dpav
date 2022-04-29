from .vbuffer import VBuffer
from datetime import datetime
from math import sin, cos, pi
import numpy as np
import pygame

try:
    from scipy.io import wavfile
except ModuleNotFoundError:
    pass


def _debug_out(msg):
    date_time = datetime.now()
    date = date_time.strftime("%Y%m%d")
    time = date_time.strftime("%H:%M:%S")

    msg = "{} | {}\n".format(time, msg)
    filename = "./logs/{}.txt".format(date)
    with open(filename, "a") as file:
        file.write(msg)


def draw_rectangle(vbuffer, color, pt1, pt2):
    pts = [pt1, pt2]

    # error checking
    if type(vbuffer) != VBuffer and type(vbuffer) != np.ndarray:
        raise TypeError("arg1 must be of type vbuffer or numpy.ndarray")

    if type(color) != int or color < 0 or color > 16777215:
        raise ValueError("arg2 must be of type integer in range 0-16777215")

    for pt in pts:
        if (
            ((type(pt) != tuple) and (type(pt) != list))
            or (len(pt) > 2)
            or (len(pt) < 2)
        ):
            raise TypeError("arg3 & arg4 must be a tuple or list of 2 int elements")
        for val in pt:
            if type(val) != int:
                raise TypeError("arg3 & arg4 must be a tuple or list of 2 int elements")

    if type(vbuffer) == VBuffer:
        buf = vbuffer.buffer
    elif type(vbuffer) == np.ndarray:
        buf = vbuffer

    lowx, highx = min(pt1[0], pt2[0]), max(pt1[0], pt2[0])
    lowy, highy = min(pt1[1], pt2[1]), max(pt1[1], pt2[1])

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
    ret = np.zeros((arr.shape[0], arr.shape[1]))

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            red = arr[i, j, 0] << 16
            green = arr[i, j, 1] << 8
            blue = arr[i, j, 2]
            ret[i, j] = red + green + blue
    return ret


def get_note_from_string(string, octave):
    """
    Given a string representing a note, this will return a hz
    IN: string representing the note e.g. Ab, C, E#
    OUT: returns hz
    """
    notes = {"A": -3, "B": -1, "C": 0, "D": 2, "E": 4, "F": 5, "G": 7}
    tone = None
    if len(string) > 0:
        if string[0].upper() in notes:
            tone = notes[string[0]]
        for each in string:
            if each == "b":
                tone -= 1
            elif each == "#":
                tone += 1
        # 60 is midi middle C
        # If we want HZ of note, we take notedistance=midiread-60
        # then do 261.625565 * 2 ** (notedistance/12)
        # see this for tunings: http://techlib.com/reference/musical_note_frequencies.htm#:~:text=Starting%20at%20any%20note%20the,away%20from%20the%20starting%20note.
        # C4 is middle C

    # tone needs to be distance from C
    octavedisc = octave - 4
    tone = 12 * octavedisc + tone
    hz = 261.625565 * 2 ** (tone / 12)
    return hz


# Please fucking god find a better name
def sixteenWavtoRawData(wavefile):
    """
    takes in a string path/name of a wav file, converts it to numpy array
    """
    samplerate, data = wavfile.read(wavefile)
    return samplerate, data


def replace_color(vb: VBuffer, replaced_color: int, new_color: int):
    """
    Replace all pixels of value replaced_color with new_color in a visual
    buffer vb.
    """
    vb.buffer = np.where(vb.buffer == replaced_color, new_color, vb.buffer)


def flip_horizontally(vb: VBuffer) -> VBuffer:
    flipped_vb = VBuffer(vb.dimensions)
    for x in range(len(flipped_vb)):
        for y in range(len(flipped_vb[x])):
            xp = len(vb) - x - 1
            flipped_vb[x, y] = vb[xp, y]
    return flipped_vb


def flip_vertically(vb: VBuffer) -> VBuffer:
    flipped_vb = VBuffer(vb.dimensions)
    for x in range(len(flipped_vb)):
        for y in range(len(flipped_vb[x])):
            yp = len(vb[x]) - y - 1
            flipped_vb[x, y] = vb[x, yp]
    return flipped_vb


def translate(vb: VBuffer, x_translation: int, y_translation: int) -> (VBuffer):
    trans_vb = VBuffer(vb.dimensions)
    for x in range(len(trans_vb)):
        for y in range(len(trans_vb[x])):
            if (0 <= x + x_translation < len(trans_vb)) and (
                0 <= y + y_translation < len(trans_vb[x])
            ):
                trans_vb[x + x_translation, y + y_translation] = vb[x, y]
    return trans_vb


"""
def rotate(vb: VBuffer, degrees: int, point: tuple) -> (VBuffer):
    rot_vb = VBuffer(vb.dimensions)
    angle = degrees * (pi / 180.0)
    for x in range(len(rot_vb)):
        for y in range(len(rot_vb[x])):
            xp = int((x - point[0]) * cos(angle) - (y - point[1]) * sin(angle) + point[0])
            yp = int((x - point[0]) * sin(angle) + (y - point[1]) * cos(angle) + point[1])
            if (0 <= xp < len(rot_vb)) and (0 <= yp < len(rot_vb[x])):
                rot_vb[xp, yp] = vb[x, y]
    return rot_vb
"""


def draw_line(vb: VBuffer, p0: list, p1: list, color: int):
    """
    Draws a line on a visual buffer from p0 to p1 using Bresenham's algorithm
    """
    (x0, y0) = p0
    (x1, y1) = p1
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    while True:
        vb.buffer[x0, y0] = color
        if (x0 == x1) and (y0 == y1):
            break
        e2 = 2 * err

        if e2 >= dy:
            if x0 == x1:
                break
            err = err + dy
            x0 = x0 + sx

        if e2 <= dx:
            if y0 == y1:
                break
            err = err + dx
            y0 = y0 + sy


def draw_polygon(vb: VBuffer, vertices: list, color: int):
    """
    Draws a polygon in a visual buffer with the given vertices utilizing the
    order in which they are given.
    """
    for i in range(0, len(vertices) - 1):
        draw_line(vb, vertices[i], vertices[i + 1], color)
    draw_line(vb, vertices[-1], vertices[0], color)


def draw_circle(vb: VBuffer, center: list, r: float, color: int):
    """
    Draws a circle onto a visual buffer of a specified color and radius
    around a given center point using Bresenham's algorithm.
    """
    center_x = center[0]
    center_y = center[1]
    x = 0
    y = r
    d = 3 - (2 * r)

    vb.buffer[center_x + x][center_y + y] = color
    vb.buffer[center_x - x][center_y + y] = color
    vb.buffer[center_x + x][center_y - y] = color
    vb.buffer[center_x - x][center_y - y] = color
    vb.buffer[center_x + y][center_y + x] = color
    vb.buffer[center_x - y][center_y + x] = color
    vb.buffer[center_x + y][center_y - x] = color
    vb.buffer[center_x - y][center_y - x] = color

    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6

        vb.buffer[center_x + x][center_y + y] = color
        vb.buffer[center_x - x][center_y + y] = color
        vb.buffer[center_x + x][center_y - y] = color
        vb.buffer[center_x - x][center_y - y] = color
        vb.buffer[center_x + y][center_y + x] = color
        vb.buffer[center_x - y][center_y + x] = color
        vb.buffer[center_x + y][center_y - x] = color
        vb.buffer[center_x - y][center_y - x] = color


def fill(vb: VBuffer, color: int, vertices):
    """
    Fills a polygon defined by a set of vertices with a color.
    """
    (dimx, dimy) = vb.get_dimensions()
    for i in range(dimx):
        for j in range(dimy):
            if point_in_polygon(i, j, vertices):
                vb.buffer[i][j] = color


def point_in_polygon(x: int, y: int, vertices) -> bool:
    """
    Uses the Even-Odd Rule to determine whether or not the pixel at coordinate
    (x,y) is inside the polygon defined by a set of vertices.
    """
    num = len(vertices)
    j = num - 1
    c = False
    for i in range(num):
        if (x == vertices[i][0]) and (y == vertices[i][1]):
            return True
        if (vertices[i][1] > y) != (vertices[j][1] > y):
            slope = (x - vertices[i][0]) * (vertices[j][1] - vertices[i][1]) - (
                vertices[j][0] - vertices[i][0]
            ) * (y - vertices[i][1])
            if slope == 0:
                return True
            if (slope < 0) != (vertices[j][1] < vertices[i][1]):
                c = not c
        j = i
    return c
