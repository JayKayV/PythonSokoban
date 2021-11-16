import pygame, sys
from content import menu

pygame.init()

scr_size = (760, 760)
screen = pygame.display.set_mode(scr_size)

pygame.display.set_caption('Sokoban')

current_scene = menu.MenuScene(scr_size)

while True:
    mouseInput = None
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type == pygame.MOUSEBUTTONUP:
            mouseInput = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()
    current_scene.update(keys, mouseInput)

    #screen.fill((0, 0, 0))
    current_scene.blit(screen)
    pygame.display.update()

    current_scene = current_scene.next
