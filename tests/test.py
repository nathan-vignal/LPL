
import numpy as np
import matplotlib.pyplot as plt
import math
import random

import matplotlib; matplotlib.use("TkAgg")  # needed on pycharm
from matplotlib import pyplot as plt
from matplotlib import animation


def rotatingGraph(pos, value):
    x = pos[0]
    y = pos[1]

    # ignoring signs
    xNegative = False
    yNegative = False
    if x < 0:
        xNegative = True
        x = -x
    if y < 0:
        yNegative = True
        y = -y

    if x != 0:
        leadingCoef = y / x
    else:
        leadingCoef = 9999999

    deltaH = value
    deltaX = math.sqrt((deltaH ** 2) / (1 + (leadingCoef ** 2)))
    deltaY = deltaX * leadingCoef

    if deltaH < 0:
        deltaX = -deltaX
        deltaY = - deltaY

    if yNegative:
        if xNegative:
            return -(x + deltaX), -(y + deltaY)
        return (x + deltaX), -(y + deltaY)
    if xNegative:
        return -(x + deltaX), (y + deltaY)
    return x + deltaX, y + deltaY


print(rotatingGraph((-0.017449798320796746, -0.4996954117645704), -0.5))

