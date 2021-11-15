import pygame, game, sys
pygame.init()

scr_size = (1280, 720)
screen = pygame.display.set_mode(scr_size)

pygame.display.set_caption('Sokoban')

current_scene = game.gameScene('levels/example_level.xml', '3', scr_size)

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
