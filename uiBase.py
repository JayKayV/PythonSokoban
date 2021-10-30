import xml.etree.ElementTree as et

class UiObj:
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


class Button(UiObj):
    canHover = False
    surf = None
    hoverSurf = None
    def __init__(self, pos, size, name):
        super().__init__(pos, size, name)

    def set_rect(self, scr):
        self.rect = scr.blit(self.surf, self.pos)

    def is_hover(self, mpos):
        return self.rect.collidepoint(mpos) and self.canHover

    def blit(self, mpos=(0, 0)):
        if self.is_hover(mpos):
            return self.hoverSurf, self.rect
        return self.surf, self.rect

