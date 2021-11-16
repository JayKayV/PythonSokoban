import xml.etree.ElementTree as et
from datetime import datetime

class UiObj:
    visible = False
    xmlObj = None

    def __init__(self, pos, size, name):
        if not isinstance(pos, tuple) and not isinstance(pos, list):
            raise TypeError('position must be in tuple or list')
        if not isinstance(size, tuple) and not isinstance(size, list):
            raise TypeError('size must be in tuple or list')
        self.pos = pos
        self.size = size
        self.name = name

    def blit(self, surf):
        return "pls update this!"

    def animation(self, dt):
        return "pls update this!"

    @staticmethod
    def loadFromXml(xml_obj):
        return "pls update this!"

class Layer:
    def __init__(self, scr_size):
        if not isinstance(scr_size, tuple):
            raise ValueError('Must initiaze scr_size')
        elif not (isinstance(scr_size[0], int) and isinstance(scr_size[1], int)):
            raise TypeError('Tuple must contain int type')

        self.screensize = scr_size
        self.oldtime = datetime.now()

    def load(self):
        return "pls update this!"

    def update(self, actions):
        return "pls update this!"

    def blit(self, surf=None):
        return "pls update this!"

class Button(UiObj):
    canHover = False
    surf = None
    hoverSurf = None
    def __init__(self, pos, size, name):
        super().__init__(pos, size, name)

    def set_rect(self, scr):
        self.rect = scr.blit(self.surf, self.pos)

    def collide(self, pos):
        return self.rect.collidepoint(pos)

    def is_hover(self, mpos):
        return self.collide(mpos) and self.canHover

    def blit(self, mpos=(0, 0)):
        if self.is_hover(mpos):
            return self.hoverSurf, self.rect
        return self.surf, self.rect

