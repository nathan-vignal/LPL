
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import copy
import matplotlib; matplotlib.use("TkAgg")  # needed on pycharm
from matplotlib import pyplot as plt
from matplotlib import animation


def rotate(pos, theta):
   rotationMatrix = np.array([
       [math.cos(theta), -math.sin(theta)],
       [math.sin(theta), math.cos(theta)]]
   )
   return tuple(np.dot(pos, rotationMatrix))



#############

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))

dial = plt.Circle((0, 0), 1, fill=False, edgecolor="black")
#beat = plt.Circle((0, 0), 0.8, fc='red')

position = (0, 1)
cursor = plt.Circle(position, 0.1, fc='black')

def init():
    ax.add_patch(dial)
    cursor.center = position
    ax.add_patch(cursor)

    # ax.add_patch(beat)
    return cursor, dial  # beat, dial,


def animate(i):
    global position
    position = rotate(position, math.pi/90)

    adjustedPosition = rotatingGraph(copy.copy(position), 0)

    cursor.center = adjustedPosition

    # beat.set_radius(random.random())

    return cursor, dial  # dial, #beat


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
    deltaX = math.sqrt((deltaH**2) / (1+(leadingCoef)**2))
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





anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames=120,
                               interval=16,
                               blit=True)

plt.show()

