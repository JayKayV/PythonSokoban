import pygame, helper
from helper import color as hc
pygame.init()
from uiBase import Button, UiObj

"""
ImgButton can also implement as StaticImg (i.e just leave hover_img = 'None'
when doing so, blitting ImgButton will only display surf
The same can be said for TextButton 
"""


class ImgButton(Button):
    def __init__(self, pos, size, name, img, hover_img = "None"):
        super().__init__(pos, size, name)
        if img == 'None':
            raise ValueError('path to img can not be null')
        self.surf = pygame.image.load(img)
        if hover_img != 'None':
            self.canHover = True
            self.hoverSurf = pygame.image.load(hover_img)

    @staticmethod
    def loadFromXml(xml_obj):
        pos = (int(xml_obj.attrib["x"]), int(xml_obj.attrib["y"]))
        size = (int(xml_obj.attrib["width"]), int(xml_obj.attrib["height"]))
        name = xml_obj.attrib["name"]
        path_to_img = xml_obj.attrib["src"]
        path_to_hover_img = xml_obj.attrib["hover-src"]
        return ImgButton(pos, size, name, path_to_img, path_to_hover_img)

class TextButton(Button):
    hoverSurf = None
    def __init__(self, pos, size, name, bck_grnd, font, font_size, color, text,
                 hover_background = 'None', hover_color = 'None'):
        super().__init__(pos, size, name)
        self.bck_grnd = bck_grnd
        self.font = font
        self.font_size = font_size
        self.color = color
        self.text = text

        self.gamefont = pygame.font.Font(self.font, font_size)
        self.textimg = self.gamefont.render(self.text, 1, hc[color])

        #calc for auto align center
        textsize = self.gamefont.size(self.text)
        if self.size == (0, 0):
            if self.bck_grnd == "None":
                self.size = textsize
            else:
                self.size = pygame.image.load(self.bck_grnd).get_size()
        textpos = helper.aligncenter(self.size, textsize)
        self.surf = pygame.Surface(self.size)

        if self.bck_grnd != "None":
            bck_surf = pygame.image.load(self.bck_grnd)
            self.surf.blit(bck_surf, (0, 0))
        self.surf.blit(self.textimg, textpos)

        #for hover
        if hover_background != "None":
            self.canHover = True
            self.hoverSurf = pygame.Surface(self.size)
            hover_surf = pygame.image.load(hover_background)
            self.hoverSurf.blit(hover_surf, (0, 0))
        if hover_color != "None":
            self.canHover = True
            hover_textimg = self.gamefont.render(self.text, 1, hc[hover_color])
            if hover_background == "None":
                self.hoverSurf = self.surf.copy()
                self.hoverSurf.blit(hover_textimg, textpos)
            else:
                self.hoverSurf.blit(hover_textimg, textpos)

    @staticmethod
    def loadFromXml(xml_obj):
        pos = (int(xml_obj.attrib["x"]), int(xml_obj.attrib["y"]))
        size = (int(xml_obj.attrib["width"]), int(xml_obj.attrib["height"]))
        name = xml_obj.attrib["name"]
        bck_grnd = xml_obj.attrib["background"]
        font = xml_obj.attrib["font"]
        font_size = int(xml_obj.attrib["font-size"])
        color = xml_obj.attrib["color"]
        text = xml_obj.text
        hover_background, hover_color = "None", "None"
        if "hover-background" in xml_obj.attrib:
            hover_background = xml_obj.attrib["hover-background"]
        if "hover-text" in xml_obj.attrib:
            hover_color = xml_obj.attrib["hover-text"]
        return TextButton(pos, size, name, bck_grnd, font, font_size, color, text, hover_background, hover_color)

    def onclick(self, mpos, func, *args):
        if self.rect.collidepoint(mpos):
            func(*args)

class UpdateableText(TextButton):
    #todo here
    #update surf
    def update(self, new_value):
        self.text = new_value

class KeyInput(UiObj):
    isActive = False
    xml_path = 'config/keys.xml'
    def __init__(self, static_obj, update_obj):
        self.static_obj = static_obj
        self.update_obj = update_obj

    @staticmethod
    def loadFromXml(xml_obj):
        static = xml_obj[0]
        update = xml_obj[1]
        return KeyInput(static, update)








