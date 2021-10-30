import xml.etree.ElementTree as et
import pygame
from ui import TextButton
pygame.init()

pygame.display.set_caption('test')
scr = pygame.display.set_mode((300, 200))

root = et.parse('config/ui.xml').getroot()
mybutton = TextButton.loadFromXml(root[0][0])
mybutton.set_rect(scr)

def _debug(*args):
    print('YES!')

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()

        if e.type == pygame.MOUSEBUTTONUP:
            mpos = pygame.mouse.get_pos()
            mybutton.onclick(mpos, _debug, None)

    mpos = pygame.mouse.get_pos()
    bimg, bpos = mybutton.blit(mpos)
    scr.blit(bimg, bpos)
    pygame.display.update(mybutton.rect)


