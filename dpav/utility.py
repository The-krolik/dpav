from .vbuffer import VBuffer
from datetime import datetime
from enum import Enum
from enum import IntEnum
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
    (dim_x, dim_y) = vb.get_dimensions()
    for i in range(dim_x):
        for j in range(dim_y):
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


# 8x8 Character ROM based on the IBM PC CGA Font
# Uses 64-bit integer to encode a 8x8 binary array
# See Code Page 437

CHARACTER_ROM_CGA_8x8 = [
    0x0000000000000000,  # 0x00 NUL
    0x7e8199bd81a5817e,  # 0x01 ☺
    0x7effe7c3ffdbff7e,  # 0x02 ☻
    0x00081c3e7f7f7f36,  # 0x03 ♥
    0x00081c3e7f3e1c08,  # 0x04 ♦
    0x1c086b7f7f1c3e1c,  # 0x05 ♣
    0x1c083e7f3e1c0808,  # 0x06 ♠
    0x0000183c3c180000,  # 0x07 •
    0xffffe7c3c3e7ffff,  # 0x08 ◘
    0x003c664242663c00,  # 0x09 ○
    0xffc399bdbd99c3ff,  # 0x0A ◙
    0x1e333333bef0e0f0,  # 0x0B ♂
    0x187e183c6666663c,  # 0x0C ♀
    0x070f0e0c0cfcccfc,  # 0x0D ♪
    0x0367e6c6c6fec6fe,  # 0x0E ♫
    0x18db3ce7e73cdb18,  # 0x0F ☼
    0x0001071f7f1f0701,  # 0x10 ►
    0x0040707c7f7c7040,  # 0x11 ◄
    0x183c7e18187e3c18,  # 0x12 ↕
    0x0066006666666666,  # 0x13 ‼
    0x00d8d8d8dedbdbfe,  # 0x14 ¶
    0x1e331c36361cc67c,  # 0x15 §
    0x007e7e7e00000000,  # 0x16 ▬
    0xff183c7e187e3c18,  # 0x17 ↨
    0x00181818187e3c18,  # 0x18 ↑
    0x00183c7e18181818,  # 0x19 ↓
    0x000018307f301800,  # 0x1A →
    0x00000c067f060c00,  # 0x1B ←
    0x00007f0303030000,  # 0x1C ∟
    0x00002466ff662400,  # 0x1D ↔
    0x0000ffff7e3c1800,  # 0x1E ▲
    0x0000183c7effff00,  # 0x1F ▼
    0x0000000000000000,  # 0x20 Space
    0x000c000c0c1e1e0c,  # 0x21 !
    0x0000000000363636,  # 0x22 "
    0x0036367f367f3636,  # 0x23 #
    0x000c1f301e033e0c,  # 0x24 $
    0x0063660c18336300,  # 0x25 %
    0x006e333b6e1c361c,  # 0x26 &
    0x0000000000030606,  # 0x27 '
    0x00180c0606060c18,  # 0x28 (
    0x00060c1818180c06,  # 0x29 )
    0x0000663cff3c6600,  # 0x2A *
    0x00000c0c3f0c0c00,  # 0x2B +
    0x060c0c0000000000,  # 0x2C ,
    0x000000003f000000,  # 0x2D -
    0x000c0c0000000000,  # 0x2E .
    0x000103060c183060,  # 0x2F /
    0x003e676f7b73633e,  # 0x30 0
    0x003f0c0c0c0c0e0c,  # 0x31 1
    0x003f33061c30331e,  # 0x32 2
    0x001e33301c30331e,  # 0x33 3
    0x0078307f33363c38,  # 0x34 4
    0x001e3330301f033f,  # 0x35 5
    0x001e33331f03061c,  # 0x36 6
    0x000c0c0c1830333f,  # 0x37 7
    0x001e33331e33331e,  # 0x38 8
    0x000e18303e33331e,  # 0x39 9
    0x000c0c00000c0c00,  # 0x3A :
    0x060c0c00000c0c00,  # 0x3B ;
    0x00180c0603060c18,  # 0x3C <
    0x00003f00003f0000,  # 0x3D =
    0x00060c1830180c06,  # 0x3E >
    0x000c000c1830331e,  # 0x3F >
    0x001e037b7b7b633e,  # 0x40 @
    0x0033333f33331e0c,  # 0x41 A
    0x003f66663e66663f,  # 0x42 B
    0x003c66030303663c,  # 0x43 C
    0x001f36666666361f,  # 0x44 D
    0x007f46161e16467f,  # 0x45 E
    0x000f06161e16467f,  # 0x46 F
    0x007c66730303663c,  # 0x47 G
    0x003333333f333333,  # 0x48 H
    0x001e0c0c0c0c0c1e,  # 0x49 I
    0x001e333330303078,  # 0x4A J
    0x006766361e366667,  # 0x4B K
    0x007f66460606060f,  # 0x4C L
    0x0063636b7f7f7763,  # 0x4D M
    0x006363737b6f6763,  # 0x4E N
    0x001c36636363361c,  # 0x4F O
    0x000f06063e66663f,  # 0x50 P
    0x00381e3b3333331e,  # 0x51 Q
    0x006766363e66663f,  # 0x52 R
    0x001e33180c06331e,  # 0x53 S
    0x001e0c0c0c0c2d3f,  # 0x54 T
    0x003f333333333333,  # 0x55 U
    0x000c1e3333333333,  # 0x56 V
    0x0063777f6b636363,  # 0x57 W
    0x0063361c1c366363,  # 0x58 X
    0x001e0c0c1e333333,  # 0x59 Y
    0x007f664c1831637f,  # 0x5A Z
    0x001e06060606061e,  # 0x5B [
    0x00406030180c0603,  # 0x5C \
    0x001e18181818181e,  # 0x5D ]
    0x0000000063361c08,  # 0x5E ^
    0xff00000000000000,  # 0x5F _
    0x0000000000180c0c,  # 0x60 `
    0x006e333e301e0000,  # 0x61 a
    0x003b66663e060607,  # 0x62 b
    0x001e3303331e0000,  # 0x63 c
    0x006e33333e303038,  # 0x64 d
    0x001e033f331e0000,  # 0x65 e
    0x000f06060f06361c,  # 0x66 f
    0x1f303e33336e0000,  # 0x67 g
    0x006766666e360607,  # 0x68 h
    0x001e0c0c0c0e000c,  # 0x69 i
    0x1e33333030300030,  # 0x6A j
    0x0067361e36660607,  # 0x6B k
    0x001e0c0c0c0c0c0e,  # 0x6C l
    0x00636b7f7f330000,  # 0x6D m
    0x00333333331f0000,  # 0x6E n
    0x001e3333331e0000,  # 0x6F o
    0x0f063e66663b0000,  # 0x70 p
    0x78303e33336e0000,  # 0x71 q
    0x000f06666e3b0000,  # 0x72 r
    0x001f301e033e0000,  # 0x73 s
    0x00182c0c0c3e0c08,  # 0x74 t
    0x006e333333330000,  # 0x75 u
    0x000c1e3333330000,  # 0x76 v
    0x00367f7f6b630000,  # 0x77 w
    0x0063361c36630000,  # 0x78 x
    0x1f303e3333330000,  # 0x79 y
    0x003f260c193f0000,  # 0x7A z
    0x00380c0c070c0c38,  # 0x7B {
    0x0018181800181818,  # 0x7C |
    0x00070c0c380c0c07,  # 0x7D }
    0x0000000000003b6e,  # 0x7E ~
    0x007f6363361c0800,  # 0x7F ⌂
    0x1e30181e3303331e,  # 0x80 Ç
    0x007e333333003300,  # 0x81 ü
    0x001e033f331e0038,  # 0x82 é
    0x00fc667c603cc37e,  # 0x83 â
    0x007e333e301e0033,  # 0x84 ä
    0x007e333e301e0007,  # 0x85 à
    0x007e333e301e0c0c,  # 0x86 å
    0x1c301e03031e0000,  # 0x87 ç
    0x003c067e663cc37e,  # 0x88 ê
    0x001e033f331e0033,  # 0x89 ë
    0x001e033f331e0007,  # 0x8A è
    0x001e0c0c0c0e0033,  # 0x8B ï
    0x003c1818181c633e,  # 0x8C î
    0x001e0c0c0c0e0007,  # 0x8D ì
    0x0063637f63361c63,  # 0x8E Ä
    0x00333f331e000c0c,  # 0x8F Å
    0x003f061e063f0038,  # 0x90 É
    0x00fe33fe30fe0000,  # 0x91 æ
    0x007333337f33367c,  # 0x92 Æ
    0x001e33331e00331e,  # 0x93 ô
    0x001e33331e003300,  # 0x94 ö
    0x001e33331e000700,  # 0x95 ò
    0x007e33333300331e,  # 0x96 û
    0x007e333333000700,  # 0x97 ù
    0x1f303e3333003300,  # 0x98 ÿ
    0x00183c66663c18c3,  # 0x99 Ö
    0x001e333333330033,  # 0x9A Ü
    0x18187e03037e1818,  # 0x9B ¢
    0x003f67060f26361c,  # 0x9C £
    0x0c0c3f0c3f1e3333,  # 0x9D ¥
    0xe363f3635f33331f,  # 0x9E ₧
    0x0e1b18183c18d870,  # 0x9F ƒ
    0x007e333e301e0038,  # 0xA0 á
    0x001e0c0c0c0e001c,  # 0xA1 í
    0x001e33331e003800,  # 0xA2 ó
    0x007e333333003800,  # 0xA3 ú
    0x003333331f001f00,  # 0xA4 ñ
    0x00333b3f3733003f,  # 0xA5 Ñ
    0x00007e007c36363c,  # 0xA6 ª
    0x00003e001c36361c,  # 0xA7 º
    0x001e3303060c000c,  # 0xA8 ¿
    0x000003033f000000,  # 0xA9 ⌐
    0x000030303f000000,  # 0xAA ¬
    0xf03366cc7b3363c3,  # 0xAB ½
    0xc0f3f6ecdb3363c3,  # 0xAC ¼
    0x0018181818001818,  # 0xAD ¡
    0x0000cc663366cc00,  # 0xAE «
    0x00003366cc663300,  # 0xAF »
    0x1144114411441144,  # 0xB0 ░
    0x55aa55aa55aa55aa,  # 0xB1 ▒
    0x77dbeedb77dbeedb,  # 0xB2 ▓
    0x1818181818181818,  # 0xB3 │
    0x1818181f18181818,  # 0xB4 ┤
    0x1818181f181f1818,  # 0xB5 ╡
    0x6c6c6c6f6c6c6c6c,  # 0xB6 ╢
    0x6c6c6c7f00000000,  # 0xB7 ╖
    0x1818181f181f0000,  # 0xB8 ╕
    0x6c6c6c6f606f6c6c,  # 0xB9 ╣
    0x6c6c6c6c6c6c6c6c,  # 0xBA ║
    0x6c6c6c6f607f0000,  # 0xBB ╗
    0x0000007f606f6c6c,  # 0xBC ╝
    0x0000007f6c6c6c6c,  # 0xBD ╜
    0x0000001f181f1818,  # 0xBE ╛
    0x1818181f00000000,  # 0xBF ┐
    0x000000f818181818,  # 0xC0 └
    0x000000ff18181818,  # 0xC1 ┴
    0x181818ff00000000,  # 0xC2 ┬
    0x181818f818181818,  # 0xC3 ├
    0x000000ff00000000,  # 0xC4 ─
    0x181818ff18181818,  # 0xC5 ┼
    0x181818f818f81818,  # 0xC6 ╞
    0x6c6c6cec6c6c6c6c,  # 0xC7 ╟
    0x000000fc0cec6c6c,  # 0xC8 ╚
    0x6c6c6cec0cfc0000,  # 0xC9 ╔
    0x000000ff00ef6c6c,  # 0xCA ╩
    0x6c6c6cef00ff0000,  # 0xCB ╦
    0x6c6c6cec0cec6c6c,  # 0xCC ╠
    0x000000ff00ff0000,  # 0xCD ═
    0x6c6c6cef00ef6c6c,  # 0xCE ╬
    0x000000ff00ff1818,  # 0xCF ╧
    0x000000ff6c6c6c6c,  # 0xD0 ╨
    0x181818ff00ff0000,  # 0xD1 ╤
    0x6c6c6cff00000000,  # 0xD2 ╥
    0x000000fc6c6c6c6c,  # 0xD3 ╙
    0x000000f818f81818,  # 0xD4 ╘
    0x181818f818f80000,  # 0xD5 ╒
    0x6c6c6cfc00000000,  # 0xD6 ╓
    0x6c6c6cff6c6c6c6c,  # 0xD7 ╫
    0x181818ff18ff1818,  # 0xD8 ╪
    0x0000001f18181818,  # 0xD9 ┘
    0x181818f800000000,  # 0xDA ┌
    0xffffffffffffffff,  # 0xDB █
    0xffffffff00000000,  # 0xDC ▄
    0x0f0f0f0f0f0f0f0f,  # 0xDD ▌
    0xf0f0f0f0f0f0f0f0,  # 0xDE ▐
    0x00000000ffffffff,  # 0xDF ▀
    0x006e3b133b6e0000,  # 0xE0 α
    0x03031f331f331e00,  # 0xE1 ß
    0x0003030303333f00,  # 0xE2 Γ
    0x0036363636367f00,  # 0xE3 π
    0x003f33060c06333f,  # 0xE4 Σ
    0x000e1b1b1b7e0000,  # 0xE5 σ
    0x03063e6666666600,  # 0xE6 µ
    0x00181818183b6e00,  # 0xE7 τ
    0x3f0c1e33331e0c3f,  # 0xE8 Φ
    0x001c36637f63361c,  # 0xE9 Θ
    0x007736366363361c,  # 0xEA Ω
    0x001e33333e180c38,  # 0xEB δ
    0x00007edbdb7e0000,  # 0xEC ∞
    0x03067edbdb7e3060,  # 0xED φ
    0x001c06031f03061c,  # 0xEE ε
    0x003333333333331e,  # 0xEF ∩
    0x00003f003f003f00,  # 0xF0 ≡
    0x003f000c0c3f0c0c,  # 0xF1 ±
    0x003f00060c180c06,  # 0xF2 ≥
    0x003f00180c060c18,  # 0xF3 ≤
    0x1818181818d8d870,  # 0xF4 ⌠
    0x0e1b1b1818181818,  # 0xF5 ⌡
    0x000c0c003f000c0c,  # 0xF6 ÷
    0x00003b6e003b6e00,  # 0xF7 ≈
    0x000000001c36361c,  # 0xF8 °
    0x0000001818000000,  # 0xF9 ∙
    0x0000001800000000,  # 0xFA ·
    0x383c3637303030f0,  # 0xFB √
    0x000000363636361e,  # 0xFC ⁿ
    0x0000001e060c180e,  # 0xFD ²
    0x00003c3c3c3c0000,  # 0xFE ■
    0x0000000000000000]  # 0xFF NBSP

# 8 x 16 Character ROM based the IBM PC VGA Font
# Uses a pair of 64-bit integers to encode two (upper and lower) 8x8 binary arrays
# See Code Page 437

CHARACTER_ROM_VGA_8x16 = [
    (0x0000000000000000, 0x0000000000000000),  # 0x00 NUL
    (0xbd8181a5817e0000, 0x000000007e818199),  # 0x01 ☺
    (0xc3ffffdbff7e0000, 0x000000007effffe7),  # 0x02 ☻
    (0x7f7f7f3600000000, 0x00000000081c3e7f),  # 0x03 ♥
    (0x7f3e1c0800000000, 0x0000000000081c3e),  # 0x04 ♦
    (0xe7e73c3c18000000, 0x000000003c1818e7),  # 0x05 ♣
    (0xffff7e3c18000000, 0x000000003c18187e),  # 0x06 ♠
    (0x3c18000000000000, 0x000000000000183c),  # 0x07 •
    (0xc3e7ffffffffffff, 0xffffffffffffe7c3),  # 0x08 ◘
    (0x42663c0000000000, 0x00000000003c6642),  # 0x09 ○
    (0xbd99c3ffffffffff, 0xffffffffffc399bd),  # 0x0A ◙
    (0x331e4c5870780000, 0x000000001e333333),  # 0x0B ♂
    (0x3c666666663c0000, 0x0000000018187e18),  # 0x0C ♀
    (0x0c0c0cfcccfc0000, 0x00000000070f0e0c),  # 0x0D ♪
    (0xc6c6c6fec6fe0000, 0x0000000367e7e6c6),  # 0x0E ♫
    (0xe73cdb1818000000, 0x000000001818db3c),  # 0x0F ☼
    (0x1f7f1f0f07030100, 0x000000000103070f),  # 0x10 ►
    (0x7c7f7c7870604000, 0x0000000040607078),  # 0x11 ◄
    (0x1818187e3c180000, 0x0000000000183c7e),  # 0x12 ↕
    (0x6666666666660000, 0x0000000066660066),  # 0x13 ‼
    (0xd8dedbdbdbfe0000, 0x00000000d8d8d8d8),  # 0x14 ¶
    (0x6363361c06633e00, 0x0000003e63301c36),  # 0x15 §
    (0x0000000000000000, 0x000000007f7f7f7f),  # 0x16 ▬
    (0x1818187e3c180000, 0x000000007e183c7e),  # 0x17 ↨
    (0x1818187e3c180000, 0x0000000018181818),  # 0x18 ↑
    (0x1818181818180000, 0x00000000183c7e18),  # 0x19 ↓
    (0x7f30180000000000, 0x0000000000001830),  # 0x1A →
    (0x7f060c0000000000, 0x0000000000000c06),  # 0x1B ←
    (0x0303000000000000, 0x0000000000007f03),  # 0x1C ∟
    (0x7f36140000000000, 0x0000000000001436),  # 0x1D ↔
    (0x3e1c1c0800000000, 0x00000000007f7f3e),  # 0x1E ▲
    (0x3e3e7f7f00000000, 0x0000000000081c1c),  # 0x1F ▼
    (0x0000000000000000, 0x0000000000000000),  # 0x20 Space
    (0x18183c3c3c180000, 0x0000000018180018),  # 0x21 !
    (0x0000002466666600, 0x0000000000000000),  # 0x22 "
    (0x36367f3636000000, 0x0000000036367f36),  # 0x23 #
    (0x603e0343633e1818, 0x000018183e636160),  # 0x24 $
    (0x1830634300000000, 0x000000006163060c),  # 0x25 %
    (0x3b6e1c36361c0000, 0x000000006e333333),  # 0x26 &
    (0x000000060c0c0c00, 0x0000000000000000),  # 0x27 '
    (0x0c0c0c0c18300000, 0x0000000030180c0c),  # 0x28 (
    (0x30303030180c0000, 0x000000000c183030),  # 0x29 )
    (0xff3c660000000000, 0x000000000000663c),  # 0x2A *
    (0x7e18180000000000, 0x0000000000001818),  # 0x2B +
    (0x0000000000000000, 0x0000000c18181800),  # 0x2C ,
    (0x7f00000000000000, 0x0000000000000000),  # 0x2D -
    (0x0000000000000000, 0x0000000018180000),  # 0x2E .
    (0x1830604000000000, 0x000000000103060c),  # 0x2F /
    (0x6b6b6363361c0000, 0x000000001c366363),  # 0x30 0
    (0x1818181e1c180000, 0x000000007e181818),  # 0x31 1
    (0x0c183060633e0000, 0x000000007f630306),  # 0x32 2
    (0x603c6060633e0000, 0x000000003e636060),  # 0x33 3
    (0x7f33363c38300000, 0x0000000078303030),  # 0x34 4
    (0x603f0303037f0000, 0x000000003e636060),  # 0x35 5
    (0x633f0303061c0000, 0x000000003e636363),  # 0x36 6
    (0x18306060637f0000, 0x000000000c0c0c0c),  # 0x37 7
    (0x633e6363633e0000, 0x000000003e636363),  # 0x38 8
    (0x607e6363633e0000, 0x000000001e306060),  # 0x39 9
    (0x0000181800000000, 0x0000000000181800),  # 0x3A :
    (0x0000181800000000, 0x000000000c181800),  # 0x3B ;
    (0x060c183060000000, 0x000000006030180c),  # 0x3C <
    (0x00007e0000000000, 0x000000000000007e),  # 0x3D =
    (0x6030180c06000000, 0x00000000060c1830),  # 0x3E >
    (0x18183063633e0000, 0x0000000018180018),  # 0x3F ?
    (0x7b7b63633e000000, 0x000000003e033b7b),  # 0x40 @
    (0x7f6363361c080000, 0x0000000063636363),  # 0x41 A
    (0x663e6666663f0000, 0x000000003f666666),  # 0x42 B
    (0x03030343663c0000, 0x000000003c664303),  # 0x43 C
    (0x66666666361f0000, 0x000000001f366666),  # 0x44 D
    (0x161e1646667f0000, 0x000000007f664606),  # 0x45 E
    (0x161e1646667f0000, 0x000000000f060606),  # 0x46 F
    (0x7b030343663c0000, 0x000000005c666363),  # 0x47 G
    (0x637f636363630000, 0x0000000063636363),  # 0x48 H
    (0x18181818183c0000, 0x000000003c181818),  # 0x49 I
    (0x3030303030780000, 0x000000001e333333),  # 0x4A J
    (0x1e1e366666670000, 0x0000000067666636),  # 0x4B K
    (0x06060606060f0000, 0x000000007f664606),  # 0x4C L
    (0x636b7f7f77630000, 0x0000000063636363),  # 0x4D M
    (0x737b7f6f67630000, 0x0000000063636363),  # 0x4E N
    (0x63636363633e0000, 0x000000003e636363),  # 0x4F O
    (0x063e6666663f0000, 0x000000000f060606),  # 0x50 P
    (0x63636363633e0000, 0x000070303e7b6b63),  # 0x51 Q
    (0x363e6666663f0000, 0x0000000067666666),  # 0x52 R
    (0x301c0663633e0000, 0x000000003e636360),  # 0x53 S
    (0x1818185a7e7e0000, 0x000000003c181818),  # 0x54 T
    (0x6363636363630000, 0x000000003e636363),  # 0x55 U
    (0x6363636363630000, 0x00000000081c3663),  # 0x56 V
    (0x6b6b636363630000, 0x0000000036777f6b),  # 0x57 W
    (0x1c1c3e3663630000, 0x000000006363363e),  # 0x58 X
    (0x183c666666660000, 0x000000003c181818),  # 0x59 Y
    (0x0c183061637f0000, 0x000000007f634306),  # 0x5A Z
    (0x0c0c0c0c0c3c0000, 0x000000003c0c0c0c),  # 0x5B [
    (0x1c0e070301000000, 0x0000000040607038),  # 0x5C \
    (0x30303030303c0000, 0x000000003c303030),  # 0x5D ]
    (0x0000000063361c08, 0x0000000000000000),  # 0x5E ^
    (0x0000000000000000, 0x0000ff0000000000),  # 0x5F _
    (0x0000000000180c0c, 0x0000000000000000),  # 0x60 `
    (0x3e301e0000000000, 0x000000006e333333),  # 0x61 a
    (0x66361e0606070000, 0x000000003e666666),  # 0x62 b
    (0x03633e0000000000, 0x000000003e630303),  # 0x63 c
    (0x33363c3030380000, 0x000000006e333333),  # 0x64 d
    (0x7f633e0000000000, 0x000000003e630303),  # 0x65 e
    (0x060f0626361c0000, 0x000000000f060606),  # 0x66 f
    (0x33336e0000000000, 0x001e33303e333333),  # 0x67 g
    (0x666e360606070000, 0x0000000067666666),  # 0x68 h
    (0x18181c0018180000, 0x000000003c181818),  # 0x69 i
    (0x6060700060600000, 0x003c666660606060),  # 0x6A j
    (0x1e36660606070000, 0x000000006766361e),  # 0x6B k
    (0x18181818181c0000, 0x000000003c181818),  # 0x6C l
    (0x6b7f370000000000, 0x00000000636b6b6b),  # 0x6D m
    (0x66663b0000000000, 0x0000000066666666),  # 0x6E n
    (0x63633e0000000000, 0x000000003e636363),  # 0x6F o
    (0x66663b0000000000, 0x000f06063e666666),  # 0x70 p
    (0x33336e0000000000, 0x007830303e333333),  # 0x71 q
    (0x666e3b0000000000, 0x000000000f060606),  # 0x72 r
    (0x06633e0000000000, 0x000000003e63301c),  # 0x73 s
    (0x0c0c3f0c0c080000, 0x00000000386c0c0c),  # 0x74 t
    (0x3333330000000000, 0x000000006e333333),  # 0x75 u
    (0x6666660000000000, 0x00000000183c6666),  # 0x76 v
    (0x6b63630000000000, 0x00000000367f6b6b),  # 0x77 w
    (0x1c36630000000000, 0x0000000063361c1c),  # 0x78 x
    (0x6363630000000000, 0x001f30607e636363),  # 0x79 y
    (0x18337f0000000000, 0x000000007f63060c),  # 0x7A z
    (0x180e181818700000, 0x0000000070181818),  # 0x7B {
    (0x1800181818180000, 0x0000000018181818),  # 0x7C |
    (0x18701818180e0000, 0x000000000e181818),  # 0x7D }
    (0x000000003b6e0000, 0x0000000000000000),  # 0x7E ~
    (0x63361c0800000000, 0x00000000007f6363),  # 0x7F ⌂
    (0x03030343663c0000, 0x00003e60303c6643),  # 0x80 Ç
    (0x3333330000330000, 0x000000006e333333),  # 0x81 ü
    (0x7f633e000c183000, 0x000000003e630303),  # 0x82 é
    (0x3e301e00361c0800, 0x000000006e333333),  # 0x83 â
    (0x3e301e0000330000, 0x000000006e333333),  # 0x84 ä
    (0x3e301e00180c0600, 0x000000006e333333),  # 0x85 à
    (0x3e301e001c361c00, 0x000000006e333333),  # 0x86 å
    (0x0606663c00000000, 0x0000003c60303c66),  # 0x87 ç
    (0x7f633e00361c0800, 0x000000003e630303),  # 0x88 ê
    (0x7f633e0000630000, 0x000000003e630303),  # 0x89 ë
    (0x7f633e00180c0600, 0x000000003e630303),  # 0x8A è
    (0x18181c0000660000, 0x000000003c181818),  # 0x8B ï
    (0x18181c00663c1800, 0x000000003c181818),  # 0x8C î
    (0x18181c00180c0600, 0x000000003c181818),  # 0x8D ì
    (0x6363361c08006300, 0x000000006363637f),  # 0x8E Ä
    (0x6363361c001c361c, 0x000000006363637f),  # 0x8F Å
    (0x3e06667f00060c18, 0x000000007f660606),  # 0x90 É
    (0x6c6e330000000000, 0x00000000761b1b7e),  # 0x91 æ
    (0x337f3333367c0000, 0x0000000073333333),  # 0x92 Æ
    (0x63633e00361c0800, 0x000000003e636363),  # 0x93 ô
    (0x63633e0000630000, 0x000000003e636363),  # 0x94 ö
    (0x63633e00180c0600, 0x000000003e636363),  # 0x95 ò
    (0x33333300331e0c00, 0x000000006e333333),  # 0x96 û
    (0x33333300180c0600, 0x000000006e333333),  # 0x97 ù
    (0x6363630000630000, 0x001e30607e636363),  # 0x98 ÿ
    (0x636363633e006300, 0x000000003e636363),  # 0x99 Ö
    (0x6363636363006300, 0x000000003e636363),  # 0x9A Ü
    (0x060606663c181800, 0x0000000018183c66),  # 0x9B ¢
    (0x06060f0626361c00, 0x000000003f670606),  # 0x9C £
    (0x187e183c66660000, 0x000000001818187e),  # 0x9D ¥
    (0x7b33231f33331f00, 0x0000000063333333),  # 0x9E ₧
    (0x187e181818d87000, 0x00000e1b18181818),  # 0x9F ƒ
    (0x3e301e00060c1800, 0x000000006e333333),  # 0xA0 á
    (0x18181c000c183000, 0x000000003c181818),  # 0xA1 í
    (0x63633e00060c1800, 0x000000003e636363),  # 0xA2 ó
    (0x33333300060c1800, 0x000000006e333333),  # 0xA3 ú
    (0x66663b003b6e0000, 0x0000000066666666),  # 0xA4 ñ
    (0x7b7f6f6763003b6e, 0x0000000063636373),  # 0xA5 Ñ
    (0x007e007c36363c00, 0x0000000000000000),  # 0xA6 ª
    (0x003e001c36361c00, 0x0000000000000000),  # 0xA7 º
    (0x060c0c000c0c0000, 0x000000003e636303),  # 0xA8 ¿
    (0x037f000000000000, 0x0000000000030303),  # 0xA9 ⌐
    (0x607f000000000000, 0x0000000000606060),  # 0xAA ¬
    (0x0c18336343030300, 0x00007c1830613b06),  # 0xAB ½
    (0x0c18336343030300, 0x000060607c797366),  # 0xAC ¼
    (0x1818180018180000, 0x00000000183c3c3c),  # 0xAD ¡
    (0x1b366c0000000000, 0x0000000000006c36),  # 0xAE «
    (0x6c361b0000000000, 0x0000000000001b36),  # 0xAF »
    (0x2288228822882288, 0x2288228822882288),  # 0xB0 ░
    (0x55aa55aa55aa55aa, 0x55aa55aa55aa55aa),  # 0xB1 ▒
    (0xeebbeebbeebbeebb, 0xeebbeebbeebbeebb),  # 0xB2 ▓
    (0x1818181818181818, 0x1818181818181818),  # 0xB3 │
    (0x1f18181818181818, 0x1818181818181818),  # 0xB4 ┤
    (0x1f181f1818181818, 0x1818181818181818),  # 0xB5 ╡
    (0x6f6c6c6c6c6c6c6c, 0x6c6c6c6c6c6c6c6c),  # 0xB6 ╢
    (0x7f00000000000000, 0x6c6c6c6c6c6c6c6c),  # 0xB7 ╖
    (0x1f181f0000000000, 0x1818181818181818),  # 0xB8 ╕
    (0x6f606f6c6c6c6c6c, 0x6c6c6c6c6c6c6c6c),  # 0xB9 ╣
    (0x6c6c6c6c6c6c6c6c, 0x6c6c6c6c6c6c6c6c),  # 0xBA ║
    (0x6f607f0000000000, 0x6c6c6c6c6c6c6c6c),  # 0xBB ╗
    (0x7f606f6c6c6c6c6c, 0x0000000000000000),  # 0xBC ╝
    (0x7f6c6c6c6c6c6c6c, 0x0000000000000000),  # 0xBD ╜
    (0x1f181f1818181818, 0x0000000000000000),  # 0xBE ╛
    (0x1f00000000000000, 0x1818181818181818),  # 0xBF ┐
    (0xf818181818181818, 0x0000000000000000),  # 0xC0 └
    (0xff18181818181818, 0x0000000000000000),  # 0xC1 ┴
    (0xff00000000000000, 0x1818181818181818),  # 0xC2 ┬
    (0xf818181818181818, 0x1818181818181818),  # 0xC3 ├
    (0xff00000000000000, 0x0000000000000000),  # 0xC4 ─
    (0xff18181818181818, 0x1818181818181818),  # 0xC5 ┼
    (0xf818f81818181818, 0x1818181818181818),  # 0xC6 ╞
    (0xec6c6c6c6c6c6c6c, 0x6c6c6c6c6c6c6c6c),  # 0xC7 ╟
    (0xfc0cec6c6c6c6c6c, 0x0000000000000000),  # 0xC8 ╚
    (0xec0cfc0000000000, 0x6c6c6c6c6c6c6c6c),  # 0xC9 ╔
    (0xff00ef6c6c6c6c6c, 0x0000000000000000),  # 0xCA ╩
    (0xef00ff0000000000, 0x6c6c6c6c6c6c6c6c),  # 0xCB ╦
    (0xec0cec6c6c6c6c6c, 0x6c6c6c6c6c6c6c6c),  # 0xCC ╠
    (0xff00ff0000000000, 0x0000000000000000),  # 0xCD ═
    (0xef00ef6c6c6c6c6c, 0x6c6c6c6c6c6c6c6c),  # 0xCE ╬
    (0xff00ff1818181818, 0x0000000000000000),  # 0xCF ╧
    (0xff6c6c6c6c6c6c6c, 0x0000000000000000),  # 0xD0 ╨
    (0xff00ff0000000000, 0x1818181818181818),  # 0xD1 ╤
    (0xff00000000000000, 0x6c6c6c6c6c6c6c6c),  # 0xD2 ╥
    (0xfc6c6c6c6c6c6c6c, 0x0000000000000000),  # 0xD3 ╙
    (0xf818f81818181818, 0x0000000000000000),  # 0xD4 ╘
    (0xf818f80000000000, 0x1818181818181818),  # 0xD5 ╒
    (0xfc00000000000000, 0x6c6c6c6c6c6c6c6c),  # 0xD6 ╓
    (0xff6c6c6c6c6c6c6c, 0x6c6c6c6c6c6c6c6c),  # 0xD7 ╫
    (0xff18ff1818181818, 0x1818181818181818),  # 0xD8 ╪
    (0x1f18181818181818, 0x0000000000000000),  # 0xD9 ┘
    (0xf800000000000000, 0x1818181818181818),  # 0xDA ┌
    (0xffffffffffffffff, 0xffffffffffffffff),  # 0xDB █
    (0xff00000000000000, 0xffffffffffffffff),  # 0xDC ▄
    (0x0f0f0f0f0f0f0f0f, 0x0f0f0f0f0f0f0f0f),  # 0xDD ▌
    (0xf0f0f0f0f0f0f0f0, 0xf0f0f0f0f0f0f0f0),  # 0xDE ▐
    (0x00ffffffffffffff, 0x0000000000000000),  # 0xDF ▀
    (0x1b3b6e0000000000, 0x000000006e3b1b1b),  # 0xE0 α
    (0x331b3333331e0000, 0x0000000033636363),  # 0xE1 ß
    (0x03030363637f0000, 0x0000000003030303),  # 0xE2 Γ
    (0x3636367f00000000, 0x0000000036363636),  # 0xE3 π
    (0x180c06637f000000, 0x000000007f63060c),  # 0xE4 Σ
    (0x1b1b7e0000000000, 0x000000000e1b1b1b),  # 0xE5 σ
    (0x6666666600000000, 0x0000000306063e66),  # 0xE6 µ
    (0x18183b6e00000000, 0x0000000018181818),  # 0xE7 τ
    (0x66663c187e000000, 0x000000007e183c66),  # 0xE8 Φ
    (0x7f6363361c000000, 0x000000001c366363),  # 0xE9 Θ
    (0x36636363361c0000, 0x0000000077363636),  # 0xEA Ω
    (0x667c30180c780000, 0x000000003c666666),  # 0xEB δ
    (0xdbdb7e0000000000, 0x0000000000007edb),  # 0xEC ∞
    (0xdbdb7e60c0000000, 0x0000000003067ecf),  # 0xED φ
    (0x063e06060c380000, 0x00000000380c0606),  # 0xEE ε
    (0x636363633e000000, 0x0000000063636363),  # 0xEF ∩
    (0x7f00007f00000000, 0x00000000007f0000),  # 0xF0 ≡
    (0x187e181800000000, 0x00000000ff000018),  # 0xF1 ±
    (0x306030180c000000, 0x000000007e000c18),  # 0xF2 ≥
    (0x0c060c1830000000, 0x000000007e003018),  # 0xF3 ≤
    (0x181818d8d8700000, 0x1818181818181818),  # 0xF4 ⌠
    (0x1818181818181818, 0x000000000e1b1b1b),  # 0xF5 ⌡
    (0x7e00181800000000, 0x0000000000181800),  # 0xF6 ÷
    (0x003b6e0000000000, 0x0000000000003b6e),  # 0xF7 ≈
    (0x0000001c36361c00, 0x0000000000000000),  # 0xF8 °
    (0x1800000000000000, 0x0000000000000018),  # 0xF9 ∙
    (0x0000000000000000, 0x0000000000000018),  # 0xFA ·
    (0x373030303030f000, 0x00000000383c3636),  # 0xFB √
    (0x0036363636361b00, 0x0000000000000000),  # 0xFC ⁿ
    (0x001f13060c1b0e00, 0x0000000000000000),  # 0xFD ²
    (0x3e3e3e3e00000000, 0x00000000003e3e3e),  # 0xFE ■
    (0x0000000000000000, 0x0000000000000000)]  # 0xFF NBSP

CHARACTER_MAP_437 = {
    "\u0000": 0x00,
    "☺": 0x01,
    "☻": 0x02,
    "♥": 0x03,
    "♦": 0x04,
    "♣": 0x05,
    "♠": 0x06,
    "•": 0x07,
    "◘": 0x08,
    "○": 0x09,
    "◙": 0x0A,
    "♂": 0x0B,
    "♀": 0x0C,
    "♪": 0x0D,
    "♫": 0x0E,
    "☼": 0x0F,
    "►": 0x10,
    "◄": 0x11,
    "↕": 0x12,
    "‼": 0x13,
    "¶": 0x14,
    "§": 0x15,
    "▬": 0x16,
    "↨": 0x17,
    "↑": 0x18,
    "↓": 0x19,
    "→": 0x1A,
    "←": 0x1B,
    "∟": 0x1C,
    "↔": 0x1D,
    "▲": 0x1E,
    "▼": 0x1F,
    " ": 0x20,
    "!": 0x21,
    "\"": 0x22,
    "#": 0x23,
    "$": 0x24,
    "%": 0x25,
    "&": 0x26,
    "'": 0x27,
    "(": 0x28,
    ")": 0x29,
    "*": 0x2A,
    "+": 0x2B,
    ",": 0x2C,
    "-": 0x2D,
    ".": 0x2E,
    "/": 0x2F,
    "0": 0x30,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "6": 0x36,
    "7": 0x37,
    "8": 0x38,
    "9": 0x39,
    ":": 0x3A,
    ";": 0x3B,
    "<": 0x3C,
    "=": 0x3D,
    ">": 0x3E,
    "?": 0x3F,
    "@": 0x40,
    "A": 0x41,
    "B": 0x42,
    "C": 0x43,
    "D": 0x44,
    "E": 0x45,
    "F": 0x46,
    "G": 0x47,
    "H": 0x48,
    "I": 0x49,
    "J": 0x4A,
    "K": 0x4B,
    "L": 0x4C,
    "M": 0x4D,
    "N": 0x4E,
    "O": 0x4F,
    "P": 0x50,
    "Q": 0x51,
    "R": 0x52,
    "S": 0x53,
    "T": 0x54,
    "U": 0x55,
    "V": 0x56,
    "W": 0x57,
    "X": 0x58,
    "Y": 0x59,
    "Z": 0x5A,
    "[": 0x5B,
    "\\": 0x5C,
    "]": 0x5D,
    "^": 0x5E,
    "_": 0x5F,
    "`": 0x60,
    "a": 0x61,
    "b": 0x62,
    "c": 0x63,
    "d": 0x64,
    "e": 0x65,
    "f": 0x66,
    "g": 0x67,
    "h": 0x68,
    "i": 0x69,
    "j": 0x6A,
    "k": 0x6B,
    "l": 0x6C,
    "m": 0x6D,
    "n": 0x6E,
    "o": 0x6F,
    "p": 0x70,
    "q": 0x71,
    "r": 0x72,
    "s": 0x73,
    "t": 0x74,
    "u": 0x75,
    "v": 0x76,
    "w": 0x77,
    "x": 0x78,
    "y": 0x79,
    "z": 0x7A,
    "{": 0x7B,
    "|": 0x7C,
    "}": 0x7D,
    "~": 0x7E,
    "⌂": 0x7F,
    "Ç": 0x80,
    "ü": 0x81,
    "é": 0x82,
    "â": 0x83,
    "ä": 0x84,
    "à": 0x85,
    "å": 0x86,
    "ç": 0x87,
    "ê": 0x88,
    "ë": 0x89,
    "è": 0x8A,
    "ï": 0x8B,
    "î": 0x8C,
    "ì": 0x8D,
    "Ä": 0x8E,
    "Å": 0x8F,
    "É": 0x90,
    "æ": 0x91,
    "Æ": 0x92,
    "ô": 0x93,
    "ö": 0x94,
    "ò": 0x95,
    "û": 0x96,
    "ù": 0x97,
    "ÿ": 0x98,
    "Ö": 0x99,
    "Ü": 0x9A,
    "¢": 0x9B,
    "£": 0x9C,
    "¥": 0x9D,
    "₧": 0x9E,
    "ƒ": 0x9F,
    "á": 0xA0,
    "í": 0xA1,
    "ó": 0xA2,
    "ú": 0xA3,
    "ñ": 0xA4,
    "Ñ": 0xA5,
    "ª": 0xA6,
    "º": 0xA7,
    "¿": 0xA8,
    "⌐": 0xA9,
    "¬": 0xAA,
    "½": 0xAB,
    "¼": 0xAC,
    "¡": 0xAD,
    "«": 0xAE,
    "»": 0xAF,
    "░": 0xB0,
    "▒": 0xB1,
    "▓": 0xB2,
    "│": 0xB3,
    "┤": 0xB4,
    "╡": 0xB5,
    "╢": 0xB6,
    "╖": 0xB7,
    "╕": 0xB8,
    "╣": 0xB9,
    "║": 0xBA,
    "╗": 0xBB,
    "╝": 0xBC,
    "╜": 0xBD,
    "╛": 0xBE,
    "┐": 0xBF,
    "└": 0xC0,
    "┴": 0xC1,
    "┬": 0xC2,
    "├": 0xC3,
    "─": 0xC4,
    "┼": 0xC5,
    "╞": 0xC6,
    "╟": 0xC7,
    "╚": 0xC8,
    "╔": 0xC9,
    "╩": 0xCA,
    "╦": 0xCB,
    "╠": 0xCC,
    "═": 0xCD,
    "╬": 0xCE,
    "╧": 0xCF,
    "╨": 0xD0,
    "╤": 0xD1,
    "╥": 0xD2,
    "╙": 0xD3,
    "╘": 0xD4,
    "╒": 0xD5,
    "╓": 0xD6,
    "╫": 0xD7,
    "╪": 0xD8,
    "┘": 0xD9,
    "┌": 0xDA,
    "█": 0xDB,
    "▄": 0xDC,
    "▌": 0xDD,
    "▐": 0xDE,
    "▀": 0xDF,
    "α": 0xE0,
    "ß": 0xE1,
    "Γ": 0xE2,
    "π": 0xE3,
    "Σ": 0xE4,
    "σ": 0xE5,
    "µ": 0xE6,
    "τ": 0xE7,
    "Φ": 0xE8,
    "Θ": 0xE9,
    "Ω": 0xEA,
    "δ": 0xEB,
    "∞": 0xEC,
    "φ": 0xED,
    "ε": 0xEE,
    "∩": 0xEF,
    "≡": 0xF0,
    "±": 0xF1,
    "≥": 0xF2,
    "≤": 0xF3,
    "⌠": 0xF4,
    "⌡": 0xF5,
    "÷": 0xF6,
    "≈": 0xF7,
    "°": 0xF8,
    "∙": 0xF9,
    "·": 0xFA,
    "√": 0xFB,
    "ⁿ": 0xFC,
    "²": 0xFD,
    "■": 0xFE,
    "\u00a0": 0xFF}

CHARACTER_ROM_TYPES = ("8x8", "8x16")


class ClassicColors16(IntEnum):

    # Regular 8 Colors
    BLACK = 0x000000
    RED = 0xBB0000
    GREEN = 0x00BB00
    YELLOW = 0xBBBB00
    BLUE = 0x0000BB
    MAGENTA = 0xBB00BB
    CYAN = 0x00BBBB
    WHITE = 0xBBBBBB

    # Bright 8 Colors
    BR_BLACK = 0x555555
    BR_RED = 0xFF5555
    BR_GREEN = 0x55FF55
    BR_YELLOW = 0xFFFF55
    BR_BLUE = 0x5555FF
    BR_MAGENTA = 0xFF55FF
    BR_CYAN = 0x55FFFF
    BR_WHITE = 0xFFFFFF


def draw_8x8_character(vb: VBuffer,
                       encoded_character: int,
                       x: int,
                       y: int,
                       fore_color,
                       back_color) -> bool:

    # Check for valid color arguments
    # Check for fore color
    if not isinstance(fore_color, (int, bool, list)):
        raise NameError("fore_color: Has to be an int, bool, list")

    # Check for fore color
    if not isinstance(back_color, (int, bool, list)):
        raise NameError("back_color:  Has to be an int, bool, list")

    # Check to see if we are drawing well out the range, that no partial drawing is possible
    if x <= -8 or y <= -8 or x >= vb.dimensions[0] or y >= vb.dimensions[1]:
        return False

    # Initialize for regular drawing conditions
    start_x_offset: int = 0
    start_y_offset: int = 0
    end_x: int = 8
    end_y: int = 8

    # Check for partial drawing conditions
    if x < 0:
        start_x_offset = abs(x)

    if y < 0:
        start_y_offset = abs(y)

    if (x + 8) >= vb.dimensions[0]:
        end_x = vb.dimensions[0] - x

    if (y + 8) >= vb.dimensions[1]:
        end_y = vb.dimensions[1] - y

    # Parse the character data from the input
    character_data = [
        (0x00000000000000FF & encoded_character) >> 0,
        (0x000000000000FF00 & encoded_character) >> 8,
        (0x0000000000FF0000 & encoded_character) >> 16,
        (0x00000000FF000000 & encoded_character) >> 24,
        (0x000000FF00000000 & encoded_character) >> 32,
        (0x0000FF0000000000 & encoded_character) >> 40,
        (0x00FF000000000000 & encoded_character) >> 48,
        (0xFF00000000000000 & encoded_character) >> 56]

    # Set the current Y position
    current_y = 0

    # Go through all the rows, starting at an offset and ending if partial drawing
    for rowData in character_data[start_y_offset:end_y]:

        # Convert row data to boolean array
        row_bool = [
            bool((0x01 & rowData) >> 0),
            bool((0x02 & rowData) >> 1),
            bool((0x04 & rowData) >> 2),
            bool((0x08 & rowData) >> 3),
            bool((0x10 & rowData) >> 4),
            bool((0x20 & rowData) >> 5),
            bool((0x40 & rowData) >> 6),
            bool((0x80 & rowData) >> 7),
        ]

        # (Re)Set the current X position
        current_x = 0
        for bit in row_bool[start_x_offset: end_x]:
            if bit:
                if isinstance(fore_color, bool):
                    pass
                elif isinstance(fore_color, int):
                    vb[x + start_x_offset + current_x][y + start_y_offset + current_y] = fore_color
                elif isinstance(fore_color, list):
                    vb[x + start_x_offset + current_x][y + start_y_offset + current_y] = fore_color[(start_x_offset + current_x + 8 * (start_y_offset + current_y)) % len(fore_color)]
            else:
                if isinstance(back_color, bool):
                    pass
                elif isinstance(back_color, int):
                    vb[x + start_x_offset + current_x][y + start_y_offset + current_y] = back_color
                elif isinstance(back_color, list):
                    vb[x + start_x_offset + current_x][y + start_y_offset + current_y] = back_color[(start_x_offset + current_x + 8 * (start_y_offset + current_y)) % len(back_color)]

            current_x += 1
        current_y += 1

    return True


def draw_8x16_character(vb: VBuffer,
                        encoded_characters: (int, int),
                        x: int,
                        y: int,
                        fore_color: int,
                        back_color: int) -> bool:
    # Draw the upper 8x8 character
    draw_8x8_character(vb, encoded_characters[0], x, y, fore_color, back_color)

    # Draw the lower 8x8 character
    draw_8x8_character(vb, encoded_characters[1], x, y + 8, fore_color, back_color)

    return True


class FontRenderer:
    # Set defaults
    character_rom = CHARACTER_ROM_CGA_8x8
    character_map = CHARACTER_MAP_437
    character_type = CHARACTER_ROM_TYPES[0]

    def draw_character(self, vb: VBuffer, encoded_character, x: int, y: int, fore_color: int, back_color: int) -> bool:
        if self.character_type == "8x8":
            draw_8x8_character(vb,
                               encoded_character,
                               x,
                               y,
                               fore_color,
                               back_color)
        elif self.character_type == "8x16":
            draw_8x16_character(vb,
                                encoded_character,
                                x,
                                y,
                                fore_color,
                                back_color)
        else:
            return False

        return True

    def draw_string(self, vb: VBuffer, string: str, x: int, y: int, fore_color: int, back_color: int) -> bool:
        current_character_x = 0

        for character in string:
            self.draw_character(vb,
                                self.character_rom[self.character_map[character]],
                                x + current_character_x,
                                y,
                                fore_color,
                                back_color)
            current_character_x += 8

        return True
