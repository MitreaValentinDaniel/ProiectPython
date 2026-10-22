import pygame

from gameLogic import GameLogic


class Scene:
    sceneImage = None

    AreaPos = (680, 0)
    AreaSize = (400, 720)
    AreaColor = (0, 0, 0, 210)

    Area = pygame.Surface(AreaSize, pygame.SRCALPHA)

    def __init__(self):
        self.gamePlay = GameLogic()
        self.sceneImage = pygame.image.load("assets/scene.jpg")


    def update(self, screen):
        screen.fill("purple")
        screen.blit(self.sceneImage, (0, 0))

        self.Area.fill(self.AreaColor)
        screen.blit(self.Area, self.AreaPos)

        self.gamePlay.update(screen)