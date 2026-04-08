from panda3d.core import LineSegs
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, TransparencyAttrib, NodePath, WindowProperties
from stanplanszy import *

class Game:
    def __init__(self, json):
        stanplanszy(self, json)