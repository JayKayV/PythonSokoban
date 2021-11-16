import pygame
import xml.etree.ElementTree as et
from content.helper import *
from content.scene import Scene, Layer
from content.game import *
pygame.init()

class MenuLayer(Layer):
    def load(self):
        self.ui = parseScene('menu')
        path = 'content/levels/example_level.xml'
        root = et.parse(path).getroot()
        self.surf = pygame.Surface(self.screensize)
        self.listSize = int(root.attrib['size'])

        self.buttonList = []
        self.buttonRect = []
        for i in range(self.listSize):
            obj = pygame.image.load('content/sprites/blue_button09.png')
            hover_obj = pygame.image.load('content/sprites/red_button08.png')
            font = pygame.font.Font('content/fonts/OpenSans-Regular.ttf', 18)
            st = str(i + 1)
            pos = aligncenter(obj.get_size(), font.size(st))
            text = font.render(st, 1, color['white'])
            obj.blit(text, pos)
            hover_obj.blit(text, pos)
            self.buttonList.append([obj, hover_obj])

            left, top = 150 + (i % 6) * 64, 300 + (i // 6) * 64
            self.buttonRect.append(self.surf.blit(obj, (left, top)))

    def update(self, mpos):
        for i in range(self.listSize):
            if self.buttonRect[i].collidepoint(mpos):
                return i + 1
        return None

    def blit(self):
        surf = pygame.Surface(self.screensize)
        for o in self.ui.values():
            mpos = pygame.mouse.get_pos()
            osurf, orect = o.blit(mpos)
            surf.blit(osurf, orect)
        for i in range(self.listSize):
            mpos = pygame.mouse.get_pos()
            if self.buttonRect[i].collidepoint(mpos):
                surf.blit(self.buttonList[i][1], self.buttonRect[i])
            else:
                surf.blit(self.buttonList[i][0], self.buttonRect[i])
        return surf

class MenuScene(Scene):
    def __init__(self, scr_size):
        super().__init__()
        self.screensize = scr_size
        self.gameLayer = MenuLayer(scr_size)
        self.gameLayer.load()

    def update(self, keyinput, mouseinput):
        if mouseinput is not None:
            chooselvl = self.gameLayer.update(mouseinput)
            if chooselvl:
                self.change(gameScene('content/levels/example_level.xml', str(chooselvl), self.screensize))
