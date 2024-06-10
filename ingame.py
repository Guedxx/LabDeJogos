from PPlay.window import *
from PPlay.animation import *


def updateAll(*args):
    for i in args:
        i.update()

def drawAll(*args):
    for i in args:
        i.draw()
