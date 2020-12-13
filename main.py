import cairo
import math
import random
import numpy as np
import sys
from SaveGifMod import SaveGif
import perlin
import os

WIDTH = 1200
HEIGHT = 1200
s = cairo.SVGSurface("surface.svg", WIDTH, HEIGHT)
c = cairo.Context(s)


def FormatColors(colorsHex):
    newArray = []
    for color in colorsHex:
        color = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
        newArray.append([color[0] / 255, color[1] / 255, color[2] / 255])
    return newArray


def SetRGB(color, a=1):
    c.set_source_rgba(color[0], color[1], color[2], a)


def Clear():
    c.save()
    SetRGB(bgColor)
    c.paint()
    c.restore()


def Draw_1(x1, width, y_max, y1, xc, yc, color1):
    SetRGB(color1)
    c.move_to(x1 + width, y_max)
    c.line_to(x1 + width, y1)
    c.line_to(xc, yc)
    c.line_to(x1, y_max)
    c.fill()


def Draw_2(x1, width, y_max, y1, xc, yc, color2):
    SetRGB(color2)
    c.move_to(x1, y_max)
    c.line_to(x1, y1)
    c.line_to(xc, yc)
    c.line_to(x1, y_max)
    c.fill()


def Draw_Lines(x1, width, y_max, y1, xc, yc, color2):
    c.move_to(x1, y1)
    c.line_to(x1 + width, y1)
    c.line_to(x1 + width, y_max)
    c.line_to(x1, y_max)
    c.move_to(x1 + width, y1)
    c.line_to(xc, yc)
    c.stroke()


def Draw_Path(x1, y1, width, color1, color2, line_width):
    y_max = WIDTH
    xc = WIDTH / 2
    yc = HEIGHT / 2
    if x < xc:
        width *= -1
    if y < yc:
        y_max = 0
    c.set_line_width(line_width)
    Draw_1(x1, width, y_max, y1, xc, yc, color1)
    Draw_2(x1, width, y_max, y1, xc, yc, color2)
    Draw_Lines(x1, width, y_max, y1, xc, yc, color2)


# number of frames
frames = 50
fileNames = []
for frame in range(0, frames):
    c.save()
    # rectangle width
    width = 5
    # gap between rectangles
    step = width * 2
    # forecolor hex
    color1 = FormatColors(["b76935"])[0]
    # backcolor hex
    color2 = FormatColors(["143642"])[0]
    bgColor = color2
    Clear()

    # increase y value each step towards center
    yIncRatio = frame * frame / (frames * frames - frames * 2)
    yInc = (HEIGHT * yIncRatio) / (WIDTH / step)
    for i in range(0, 2):
        c.translate(WIDTH / 2, HEIGHT / 2)
        c.rotate(math.pi / 2)
        c.translate(-WIDTH / 2, -HEIGHT / 2)
        for y in [HEIGHT, 0]:
            y0 = y
            for x in np.arange(width, WIDTH / 2, step):
                Draw_Path(x, y, width, color1, color2, 1)
                y -= yInc
            y = y0
            for x in np.arange(WIDTH - width, WIDTH / 2, -step):
                Draw_Path(x, y, width, color1, color2, 1)
                y -= yInc
            yInc *= -1
    # draw square in center
    r1 = 80
    r = r1 - (frame * frame / 10000 * r1)
    SetRGB(color2)
    c.translate(WIDTH / 2, HEIGHT / 2)
    c.rotate(math.pi / 4)
    c.translate(-WIDTH / 2, -HEIGHT / 2)
    c.rectangle(WIDTH / 2 - r / 2, HEIGHT / 2 - r / 2, r, r)
    c.fill()
    SetRGB(color1)
    c.rectangle(WIDTH / 2 - r / 2, HEIGHT / 2 - r / 2, r, r)
    c.set_line_width(2)
    c.stroke()
    # save file
    fileName = "output" + str(frame) + ".png"
    s.write_to_png(fileName)
    fileNames.append(fileName)
    c.restore()
# save gif
SaveGif(fileNames, "output.gif", True)
