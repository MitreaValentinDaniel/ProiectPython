import pygame

leftKey = pygame.K_a
rightKey = pygame.K_d
upKey = pygame.K_w
downKey = pygame.K_s



class GameLogic:

    leftArrow = pygame.image
    rightArrow = pygame.image
    upArrow = pygame.image
    downArrow = pygame.image
    distanceBetweenArrows = 110

    def __init__(self):

        print("Game Logic Assets initialised")
        self.leftArrow  =  pygame.image.load("assets/leftArrow.png")
        self.rightArrow = pygame.image.load("assets/rightArrow.png")
        self.upArrow    =    pygame.image.load("assets/upArrow.png")
        self.downArrow  =  pygame.image.load("assets/downArrow.png")
        pass

    def update(self, screen):
        keys = pygame.key.get_pressed()

        screen.blit(self.leftArrow,  (700,                                  720 - 80))
        screen.blit(self.downArrow,  (700 + self.distanceBetweenArrows,     720 - 80))
        screen.blit(self.upArrow,    (700 + self.distanceBetweenArrows * 2, 720 - 80))
        screen.blit(self.rightArrow, (700 + self.distanceBetweenArrows * 3, 720 - 80))


        if keys[leftKey]:
            print("LEFT")

        if keys[rightKey]:
            print("RIGHT")

        if keys[upKey]:
            print("UP")

        if keys[downKey]:
            print("DOWN")
