import pygame
from content import helper
from content.helper import color as hc
import xml.etree.ElementTree as et
pygame.init()
from content.uiBase import Button, UiObj

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
        if self.size == (0, 0):
            self.size = self.surf.get_size()
        if hover_img != 'None':
            self.canHover = True
            self.hoverSurf = pygame.image.load(hover_img)

    @staticmethod
    def loadFromXml(xml_obj):
        pos = (int(xml_obj.attrib["x"]), int(xml_obj.attrib["y"]))
        size = (int(xml_obj.attrib["width"]), int(xml_obj.attrib["height"]))
        name = xml_obj.attrib["name"]
        path_to_img = xml_obj.attrib["src"]
        path_to_hover_img = 'None'
        if 'hover-src' in xml_obj.attrib:
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
        self.textimg = self.gamefont.render(self.text, 1, hc[self.color])

        #calc for auto align center
        textsize = self.gamefont.size(self.text)
        if self.size == (0, 0):
            if self.bck_grnd == "None":
                self.size = textsize
            else:
                self.size = pygame.image.load(self.bck_grnd).get_size()
        self.textpos = helper.aligncenter(self.size, textsize)
        self.surf = pygame.Surface(self.size)

        if self.bck_grnd != "None":
            bck_surf = pygame.image.load(self.bck_grnd)
            self.surf.blit(bck_surf, (0, 0))
        self.surf.blit(self.textimg, self.textpos)

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
                self.hoverSurf.blit(hover_textimg, self.textpos)
            else:
                self.hoverSurf.blit(hover_textimg, self.textpos)

    @staticmethod
    def loadFromXml(xml_obj):
        pos = (int(xml_obj.attrib["x"]), int(xml_obj.attrib["y"]))
        size = (int(xml_obj.attrib["width"]), int(xml_obj.attrib["height"]))
        name = xml_obj.attrib["name"]
        bck_grnd = xml_obj.attrib["background"]
        font = "content/fonts/OpenSans-Regular.ttf"
        if "font" in xml_obj.attrib:
            font = xml_obj.attrib["font"]
        font_size = 16
        if "font-size" in xml_obj.attrib:
            font_size = int(xml_obj.attrib["font-size"])
        color = 'black'
        if 'color' in xml_obj.attrib:
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
    def set(self, static_text, var_text):
        self.static_text = static_text
        self.var_text = var_text

        text = self.static_text.format(self.var_text)
        self.surf.fill((0, 0, 0))
        self.textimg = self.gamefont.render(text, 1, self.color)
        self.surf.blit(self.textimg, self.textpos)

    def update(self, new_value):
        self.set(self.static_text, new_value)

    @staticmethod
    def loadFromXml(xml_obj):
        pos = (int(xml_obj.attrib["x"]), int(xml_obj.attrib["y"]))
        size = (int(xml_obj.attrib["width"]), int(xml_obj.attrib["height"]))
        name = xml_obj.attrib["name"]
        bck_grnd = xml_obj.attrib["background"]
        font = "content/fonts/OpenSans-Regular.ttf"
        if "font" in xml_obj.attrib:
            font = xml_obj.attrib["font"]
        font_size = 16
        if "font-size" in xml_obj.attrib:
            font_size = int(xml_obj.attrib["font-size"])
        color = 'black'
        if 'color' in xml_obj.attrib:
            color = xml_obj.attrib["color"]
        text = xml_obj.text
        hover_background, hover_color = "None", "None"
        if "hover-background" in xml_obj.attrib:
            hover_background = xml_obj.attrib["hover-background"]
        if "hover-text" in xml_obj.attrib:
            hover_color = xml_obj.attrib["hover-text"]
        return UpdateableText(pos, size, name, bck_grnd, font, font_size, color, text, hover_background, hover_color)

class KeyInput(UiObj):
    isActive = False
    xml_path = 'content/config/keys.xml'
    def __init__(self, static_obj, update_obj):
        self.static_obj = static_obj
        self.update_obj = update_obj

    @staticmethod
    def loadFromXml(xml_obj):
        static = xml_obj[0]
        update = xml_obj[1]
        return KeyInput(static, update)

def parseScene(scene_name):
    xml_path = 'content/config/ui.xml'
    root = et.parse(xml_path).getroot()
    scene = root.find('./scene[@name=\'{}\']'.format(scene_name))
    if scene is None:
        raise ValueError('scene name: {} doesn\'t exist in xml file'.format(scene_name))
    objs = []
    for o in scene:
        if o.tag == 'button':
            if o.attrib['type'] == 'text':
                objs.append(TextButton.loadFromXml(o))
            elif o.attrib['type'] == 'img':
                objs.append(ImgButton.loadFromXml(o))
            else:
                raise ValueError('Button have wrong type')
        elif o.tag == 'text':
            if o.attrib['type'] == 'updateable':
                objs.append(UpdateableText.loadFromXml(o))
            elif o.attrib['type'] == 'static':
                objs.append(TextButton.loadFromXml(o))
            else:
                raise ValueError('Text have wrong type')
    for o in objs:
        o.rect = pygame.rect.Rect((o.pos, o.size))
    return {obj.name:obj for obj in objs}










