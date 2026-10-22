import pygame


from scene import Scene

pygame.init()
screenWidth, screenHeight = 1280, 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
title_screen = "Petarda"
pygame.display.set_caption(title_screen)

clock = pygame.time.Clock()
running = True

scene = Scene()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    scene.update(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()