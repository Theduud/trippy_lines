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


colors = FormatColors(["355070", "6d597a", "b56576", "e56b6f", "eaac8b"])
colorsSky = FormatColors(["355070", "eaac8b"])
greens = FormatColors(["4d908e", "43aa8b", "90be6d"])
red_yellows = FormatColors(["f94144", "f3722c", "f8961e", "f9844a", "f9c74f"])
bgColor = [0, 0, 0]


def SetRGB(color, a=1):
    c.set_source_rgba(color[0], color[1], color[2], a)


def GetColorArray(startingColor, endingColor, iterations):
    r1 = startingColor[0]
    g1 = startingColor[1]
    b1 = startingColor[2]
    r2 = endingColor[0]
    g2 = endingColor[1]
    b2 = endingColor[2]
    a1 = -1
    incrementA = 0
    if len(startingColor) == 4 and len(endingColor) == 4:
        a1 = startingColor[3]
        a2 = endingColor[3]
        incrementA = (a2 - a1) / iterations
        a = a1
    incrementR = (r2 - r1) / iterations
    incrementG = (g2 - g1) / iterations
    incrementB = (b2 - b1) / iterations
    colorArray = []
    r = r1
    g = g1
    b = b1

    for i in range(0, iterations):
        if a1 >= 0:
            colorArray.append([r, g, b, a])
            a += incrementA
        else:
            colorArray.append([r, g, b])
        r += incrementR
        g += incrementG
        b += incrementB

    return colorArray


def Clear():
    c.save()
    SetRGB(bgColor)
    c.paint()
    c.restore()


def DrawSky(colors):
    i = 0
    for y in range(0, HEIGHT):
        SetRGB(colors[i])
        c.rectangle(0, y, WIDTH, 1)
        c.fill()
        i += 1


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


if __name__ == "__main__":
    frames = 100
    fileNames = []
    for frame in range(0, frames):
        c.save()
        y = HEIGHT * 3 / 4
        width = 5
        x = WIDTH - width
        color1 = random.choice(colors)
        color2 = random.choice(colors)
        while color1 == color2:
            color2 = random.choice(colors)
        color1 = colors[4]
        color2 = colors[2]
        color1 = FormatColors(["b76935"])[0]
        # pit
        color2 = FormatColors(["143642"])[0]
        bgColor = color2
        Clear()
        step = width * 2
        yIncRatio = frame * frame / 9700
        yInc = (HEIGHT * yIncRatio) / (WIDTH / step)
        rotate = True
        for i in range(0, 2):
            if rotate:
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
            if not rotate:
                c.translate(WIDTH / 2, HEIGHT / 2)
                c.rotate(math.pi / 2)
                c.translate(-WIDTH / 2, -HEIGHT / 2)
        r1 = 80
        r = r1 - (frame * frame / 10000 * r1)
        SetRGB(color2)
        c.translate(WIDTH / 2, HEIGHT / 2)
        c.rotate(math.pi / 4)
        c.translate(-WIDTH / 2, -HEIGHT / 2)
        c.rectangle(WIDTH / 2 - r / 2, HEIGHT / 2 - r / 2, r, r)
        c.fill()
        SetRGB(color1)
        # c.arc(WIDTH / 2, HEIGHT / 2, r, 0, math.pi * 2)
        c.rectangle(WIDTH / 2 - r / 2, HEIGHT / 2 - r / 2, r, r)
        c.set_line_width(2)
        c.stroke()
        fileName = "output" + str(frame) + ".png"
        s.write_to_png(fileName)
        fileNames.append(fileName)
        c.restore()
    SaveGif(fileNames, "output.gif", True)
